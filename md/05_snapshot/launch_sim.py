#!/usr/bin/env python
import sys,os
import argparse
import numpy as np
this_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_folder + "/../scripts/")
import gmx_tools.xvg

def do(cmd, comment=""):
   if len(comment) > 0:
      print comment
   print cmd
   os.system(cmd)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Remove water molecules at the end of .gro file')
   parser.add_argument('-i', '--input-folder', type=str, help="input folder where the pulling was run from", nargs='?', required=True)
   parser.add_argument('-o', '--output-folder', type=str, help="output folder", nargs='?', required=True)
   parser.add_argument('-n', '--number-of-steps', type=int, help="number of sampling steps", required=True)
   parser.add_argument('-s', '--min-distance-nm', type=float, help="minimum distance in unit nanometer", default=0.0)
   parser.add_argument('-d', '--max-distance-nm', type=float, help="maximum distance in unit nanometer", required=True)
   parser.add_argument('-N', '--node', type=str, help="node")
   parser.add_argument('-G', '--gpus', type=int, help="number of GPUs", default=4)

   if(len(sys.argv) == 1):
      parser.print_help()
      sys.exit(0)
   args = parser.parse_args()

   output_folder = os.path.abspath(args.output_folder)
   input_folder = os.path.abspath(args.input_folder)

   do("rm -rf %s" % output_folder)
   do("mkdir %s" % output_folder)
   do("mkdir %s/input" % output_folder)
   
   xvg_filename = input_folder + "/out/pullx.xvg"
   trr_filename = input_folder + "/out/sim.trr"
   tpr_filename = input_folder + "/out/sim.tpr"
   top_filename = input_folder + "/out/sim.top"
   for fn in [xvg_filename, trr_filename, tpr_filename, top_filename]:
      do("cp %s %s/input/" % (fn, output_folder))
   xvg_filename = output_folder + "/input/pullx.xvg"
   trr_filename = output_folder + "/input/sim.trr"
   tpr_filename = output_folder + "/input/sim.tpr"
   top_filename = output_folder + "/input/sim.top"
      
   [time, xcom, xset] = gmx_tools.xvg.read_xvg(xvg_filename, ncols=3)
    
   x_grid = np.linspace(args.min_distance_nm, args.max_distance_nm, args.number_of_steps)
   t_grid = np.interp(x_grid, xcom, time)

   exs = ["00_init", 
          "01_sim_pre",
          "02_sim"]
   cps = exs + ["itp", "mdp", "scripts", "log_to_file"]
   
   for x,t in zip(x_grid, t_grid):
      output_folder_sub = output_folder + ("/snap_%2.2fnm" % x)
      i_log = 0
      logfile = "%s/run.log.%i" % (output_folder_sub, i_log)
      # Do necessary initialisations
      do("mkdir %s" % output_folder_sub)
      do("mkdir %s/out" % output_folder_sub)
      do("mkdir %s/input" % output_folder_sub)
      do("cp %s %s/input/snap.top" % (top_filename, output_folder_sub))
      do("ln -sf run.log.%i %s/run.log" % (i_log, output_folder_sub), comment="Writing symlink to new log file")
      # Set up environment
      do("cp env %s/" % output_folder_sub)
      with open("%s/env" % output_folder_sub, "a") as f:
         f.write("GMXCPX_D0=\"%f\"\n" % x)
      # Write bassh script file to be submitted
      lines = []
      lines += ["#!/bin/bash\n",
                #"#SBATCH --exclude=c001,c002,c003,c004,c005,c006,c007,c008,c009,c010,c011,c012,c013,c014,c015,c016,c017,c018\n",
                "#SBATCH --exclude=c002,c006,c012\n",
                "#SBATCH --nodes=1\n",
                "#SBATCH --ntasks-per-node=1\n",
                #"#SBATCH --partition=c\n",
                "#SBATCH --partition=a\n",
                "#SBATCH --exclusive\n",
                "#SBATCH --job-name=gmx%02.1f\n" % (round(x,1)),
                "#SBATCH --output=%s\n" % logfile,
                "#SBATCH --workdir=%s\n" % output_folder_sub]
      if args.gpus > 0:
         lines.append("#SBATCH --gres=gpu:%i\n" % args.gpus)
      if args.node is not None:
         lines.append("#SBATCH --nodelist=%s\n" % args.node)
      lines.append("source ./env\n")
      for cp in cps:
         lines.append("cp -r -L %s/%s %s/\n" % (this_folder, cp, output_folder_sub))
      lines.append("echo 0 | gmx trjconv -dump %f -f %s -s %s -o %s/out/snap.gro\n" % (t, trr_filename, tpr_filename, output_folder_sub))
      lines += [("echo \"./%s\"; ./%s\n") % (ex,ex) for ex in exs]

      slurm_file = "%s/run.sh" % output_folder_sub
      with open(slurm_file, "w") as f:
         f.writelines(lines)
      do("sbatch %s" % slurm_file)
