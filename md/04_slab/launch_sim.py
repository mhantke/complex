#!/usr/bin/env python
import sys,os
import argparse

def do(cmd, comment=""):
   if len(comment) > 0:
      print comment
   print cmd
   os.system(cmd)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Remove water molecules at the end of .gro file')
   parser.add_argument('-o', '--output-folder', type=str, help="output folder", nargs='?', required=True)
   parser.add_argument('-s', '--start-at', type=int, help="start at given processing step")
   parser.add_argument('-i', '--single-step', type=int, help="run only single step")
   parser.add_argument('-m', '--mode', type=str, help="simulation mode", default="pull")
   parser.add_argument('-N', '--node', type=str, help="node", default="c022")
   if(len(sys.argv) == 1):
      parser.print_help()
      sys.exit(0)
   args = parser.parse_args()

   allowed_modes = ["pull"]
   if args.mode not in allowed_modes:
      print "ERROR: Invalid mode: %s (allowed modes: %s)" % (args.mode, str(allowed_modes))
      sys.exit(1)

   output_folder = os.path.abspath(args.output_folder)

   if args.start_at is None and args.single_step is None:
      do("rm -rf %s" % output_folder)
      do("mkdir %s" % output_folder)
      do("mkdir %s/out" % output_folder)

   lines = []
   lines += ["#!/bin/bash\n",
             "#SBATCH --exclude=c002,c012\n",
             "#SBATCH --nodelist=%s\n" % args.node,
             "#SBATCH --nodes=1\n",
             "#SBATCH --ntasks-per-node=1\n",
             "#SBATCH --gres=gpu:3\n",
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
          "11_sim",
   ]

   links = exs + ["env", "input", "itp", "mdp", "env", "scripts"]
 
   for link in links:
      lines += ["ln -sf ../%s\n" % link]
      
   if args.mode == "pull":
      lines += ["ln -sf sim_pull.mdp mdp/sim.mdp"]

   if args.start_at is not None:
      logs = [f for f in os.listdir("%s" % output_folder) if f.startswith("run.log.")]
      if len(logs) > 0:
         logs.sort()
         i_log = int(logs[-1].split(".")[-1]) + 1
      else:
         i_log = 0
      do("mv %s/run.log %s/run.log.%i" % (output_folder, output_folder, i_log), comment="Backing up old log file.")
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
