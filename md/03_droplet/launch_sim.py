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
   if(len(sys.argv) == 1):
      parser.print_help()
      sys.exit(0)
   args = parser.parse_args()

   output_folder = os.path.abspath(args.output_folder)

   if args.start_at is None:
      do("rm -r %s" % output_folder)
      do("mkdir %s" % output_folder)

   lines = []
   lines += ["#!/bin/bash\n",
             "#SBATCH --exclude=c002,c012\n",
             "#SBATCH --nodes=1\n",
             "#SBATCH --ntasks-per-node=6\n",
             "#SBATCH --cpus-per-task=4\n",
             "#SBATCH --gres=gpu:3\n",
             "#SBATCH --partition=c\n",
             "#SBATCH --exclusive\n",
             "#SBATCH --job-name=gmx\n",
             "#SBATCH --output=%s/run.log\n" % output_folder,
             "#SBATCH --workdir=%s\n" % output_folder] 

   exs = ["00_init", 
          "01_trjconv",
          "02_editconf",
          "03_solvate",
          "04_cut_water_sphere",
          "05_ions",
          "06_genion",
          "07_em_pre",
          "08_em.sh",
          "09_em_post",
          "10_nvt_pre",
          "11_nvt.sh",
          "12_nvt_post",
          "13_npt_pre",
          "14_npt.sh",
   ]
   links = exs + ["input", "itp", "mdp", "env", "scripts"]
 

   for link in links:
      lines += ["ln -s ../%s\n" % link]

   if args.start_at is not None:
      exs = [ex for ex in exs if int(ex[:2])>=args.start_at]

   for ex in exs:
      lines += ["./%s\n" % ex]

   slurm_file = "%s/run.sh" % output_folder
   with open(slurm_file, "w") as f:
      f.writelines(lines)

   do("sbatch %s" % slurm_file)
