#!/usr/bin/env python
import sys,os
import argparse

def do(cmd):
   print cmd
   os.system(cmd)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Remove water molecules at the end of .gro file')
   parser.add_argument('-o', '--output-folder', type=str, help="output folder", nargs='?', required=True)
   parser.add_argument('-s', '--start-at', type=int, help="start at given processing step")
   parser.add_argument('-i', '--single-step', type=int, help="run only single step")
   parser.add_argument('-m', '--mode', type=str, help="simulation mode", default="pull")
   if(len(sys.argv) == 1):
      parser.print_help()
      sys.exit(0)
   args = parser.parse_args()

   output_folder = os.path.abspath(args.output_folder)

   if args.start_at is None and args.single_step is None:
      do("rm -r %s" % output_folder)
      do("mkdir %s" % output_folder)

   lines = []
   lines += ["#!/bin/bash\n",
             "#SBATCH --exclude=c002,c012\n",
             "#SBATCH --nodelist=c022\n",
             "#SBATCH --nodes=1\n",
             #"#SBATCH --ntasks-per-node=6\n",
             "#SBATCH --ntasks-per-node=1\n",
             #"#SBATCH --cpus-per-task=4\n",
             #"#SBATCH --gres=gpu:2\n",
             "#SBATCH --gres=gpu:1\n",
             "#SBATCH --partition=c\n",
             "#SBATCH --exclusive\n",
             "#SBATCH --job-name=gmx\n",
             "#SBATCH --output=%s/run.log\n" % output_folder,
             "#SBATCH --workdir=%s\n" % output_folder] 

   exs = ["00_init", 
          "01_box",
          "02_solvate",
          "03_sphere",
          "04_genion_pre",
          "05_genion",
          "06_em_pre",
          "07_em",
          "08_nvt_pre",
          "09_nvt",
          "10_sim_pre",
          "11_sim_pull",
   ]


   links = exs + ["env", "input", "itp", "mdp", "env", "scripts"]
 
   for link in links:
      lines += ["ln -s -f ../%s\n" % link]

   allowed_modes = ["pull"]
   if args.mode not in allowed_modes:
      print "ERROR: Invalid mode: %s" args.mode
      return

   if args.mode == "pull":
      do("ln -s sim_pull.mdp mdp/sim.mdp")

   if args.start_at is not None:
      exs = [ex for ex in exs if int(ex[:2])>=args.start_at]

   if args.single_step is not None:
      exs = [ex for ex in exs if int(ex[:2])==args.single_step]

   for ex in exs:
      cmd = "./%s" % ex
      lines += ["echo \"%s\"\n" % cmd, "%s\n" % cmd]

   slurm_file = "%s/run.sh" % output_folder
   with open(slurm_file, "w") as f:
      f.writelines(lines)

   do("sbatch %s" % slurm_file)
