
IGM-Plus: An Integrated Genome Modeling Platform (but better!)
============================================
This is the genome modeling platform used in Frank Alber lab, Department of Microbiology, Immunology and Molecular Genetics, University of California Los Angeles. The source code is in the ```igm``` folder.
A population of single cell chromosome/whole genome single-copy/diploid structures is generated, which fully recapitulate a variety of experimental genomic and/or imaging data. It does NOT preprocess raw data.
Structures can be further processed using the [analysis package][https://github.com/alberlab/genome3danalysis] that is also available.

We are currently working on an extensive user-friendly tutorial on `GitHub.io` to help users navigate parameter choice, set up their configuration file and run the code.

We are also in the process of updating our supporting documentation. For the time being, please refer to the IGM1.0 documentation.

Cite
------------
If you use genome structures generated using this platform OR you use the platform to generate your own structure, please consider citing our work
    
 Boninsegna, L., Yildirim, A., Polles, G., Zhan, Y., Quinodoz, SA., Finn, EH., Guttman, M., Zhou, XJ., Alber, F. [Integrative genome modeling platform reveals essentiality of rare contact events in 3D genome organizations.](https://doi.org/10.1038/s41592-022-01527-x) Nat Methods 19, 938–949 (2022)

Notes
--------
We strongly advice against installing the software on a MacOS. Our experience showed that installation steps are not transferable from one version to the next, so we removed that information from this file.


What is new
---------

August 25

The current version improves upon [IGM 1.0](https://github.com/alberlab/igm), by allowing the following data to be used in the modeling:

- volume confinement from imaged single cell nuclear laminas, nucleoli, speckles
- lamina DamID when using imaged single cell nuclear laminas, nucleoli, speckles
- single cell chromating tracing data (e.g., DNA MERFISH, DNA seqFISH+):
	* tracing data as target (x,y,z) locations for selected loci, OR/AND
	* single cell paiwise distances OR/AND
	* a chromatin fiber model that is compatible with the tracing data

**Implementation changes**:

- Single chromosome genome structures can also be generated, in addition to whole genome diploid structures
- The Hi-C iterative correction can be turned off by setting a flag to 0
- Chromatin bead radius can be selected by the user, instead of defining a given chromatin-to-nucleus occupancy value
- Intra HiC and inter HiC are handled as two separate restraints
- Logging has been much improved to clearly show number of violations (and the structure displaying the most of those)
- Initialization of structures has been greatly expanded; selected loci can be initialized in pre-determined locations, and linear interpolation is used to prime the other loci
- Violations are recorded and printed out even after the initial relaxation step (no actual data here)
- Remember that a version of [LAMMPS](https://github.com/alberlab/lammpgen) with the required `fixes` is necessary.


 

Repository Organization
-----------------------

- ``` igm ```: full IGM code(s)
- ``` bin ```: IGM run master file. In particular, refer to ```igm-run.sh``` (actual submission script) and ```igm-report.sh``` (post-processing automated script)
- ``` demo ```: example inputs (.hcs, .json files) for demo run
- ``` HPC_scripts ```: create ipyparallel environment and submit actual IGM run on a SGE scheduler based HpC cluster

- ```igm-run_scheme.pdf```: is a schematic which breaks down the different computing levels of IGM and tries to explain how the different parts of the code are related to one another.
- ```IGM_documentation.pdf```: documentation (in progress)
- ```igm-config_all.json```: most comprehensive configuration file which shows parameters for all data sets that can be accommodated [update in progress]


Dependencies
------------
IGM not longer supports python 2, so you'll need a python3 environment. 
The package depends on a number of other libraries, most of them publicly 
available on pip. In addition, some other packages are required: 

- `alabtools` (`github.com/alberlab/alabtools`)
- a modified version of `LAMMPS` (forked @ `github.com/alberlab/lammpgen`) with fixes implementing user-defined forces (e.g., HarmonicLowerBound, HarmonicUpperBound, volumetric_restraint, etc)

Installation on linux
---------------------
-   Many of the alabtools and IGM dependencies can be installed with a
    few commands if you are using conda
    (https://www.anaconda.com/distribution/)
    
    Please note, we are running conda versions back from 2019. More recent versions might cause compatibility issues.
    ```
    # optional - create a new environment for igm
    conda create -n igm python=3.6
    source activate igm
    # install dependencies
    conda install pandas swig cython cgal==4.14 hdf5 h5py numpy scipy matplotlib \
                  tornado ipyparallel cloudpickle
    ```
    -   It looks like ```cgal``` version needs to be 4.14, there are some compatibility issues with latest 5.0 version.
    
    If you _really_ do not want to use conda, most of the packages can be 
    installed with pip, but it is up to you to download and build cgal and 
    hdf5, and eventually set the correct include/library paths during 
    installation.

-   Install alabtools (github.com/alberlab/alabtools)
    ```
    pip install git+https://github.com/alberlab/alabtools.git
    ```
    Note: on windows, conda CGAL generates the library, but the name depends 
    on the build, e.g CGAL-vc140-mt-4.12.lib. Go to 
    <environment directory>/Library/lib/ and copy the CGAL library to CGAL.lib
    before pip installing alabtools.
        
-   Install IGM
    ```
    pip install git+https://github.com/alberlab/igm.git 
    ```
    
-   Download and build a serial binary of the modified LAMMPS version
    ```
    git clone https://github.com/alberlab/lammpgen.git
    cd lammpgen/src
    make yes-user-genome
    make yes-molecule
    make serial
    # create a user defaults file with the path of the executable
    mkdir -p ${HOME}/.igm
    echo "[DEFAULT]" > ${HOME}/.igm/user_defaults.cfg
    echo "optimization/kernel_opts/lammps/lammps_executable = "$(pwd)/src/lmp_serial >> ${HOME}/.igm/user_defaults.cfg
    ```
    
-   If all the dependencies have been installed correctly, successful code installation should only take a few minutes.
 
-   If ```igm``` installation is successful, typing ```igm``` from the command line + ``tab`` should show the different options (```igm-run```, ```igm-report```, etc.)
    



Important notes
---------------
-   IGM uses works mostly through the file system. The reason for the design stood on the local cluster details, persistence
    of data, and minimization of memory required by the scheduler and workers. That means, in short, that scheduler, workers 
    and the node which executes the igm-run script *need to have access to a shared filesystem where all the files will be 
    located*.
-   Over the 10+ last years of simulating genome structures, we have grown to accepting  preprocessing the experimental data can be an art. For example, Hi-C raw counts need to be transformed to probability matrices. Some of these
    processes have yet to be completely and exaustively documented publicly. We are working on it, but in the meantime
    email if you need help.
  
Instructions for Use
----
 
In order to generate population of structures, the code has to be run in parallel mode, best if on HCP clusters. The scripts to do that on a SGE scheduler-based HPC resources are provided in the ```HCP_scripts``` folder. Just to get an estimate, using 250 independent cores allows generating a 1000 200 kb resolution structure population in 10-15 hour computing time, which can vary depending on the number of different data sources that are used and on the number of iterations one decides to run.

Populations of 5 or 10 structures at 200kb resolution (which is the current highest resolution we simulated) could in principle be generated serially on a "normal" desktop computer, but they have little statistical relevance. For example, 10 structures would only allow to deconvolute Hi-C contacts with probability larger than 10%, which is not sufficient for getting realistic populations. Serial executions are appropriate only at much lower resolution, as the computing burden is also much lower (an example is provided in the ```demo``` folder, see also Software demo)

Due to the necessity of HPC resources, we strongly recommend that the software be installed and run in a Linux environment. ALL the populations we have generated and analyzed were generated using a `Linux` environment. Again, please understand that We cannot guarantee full functionality on a MacOS or Windows.

In order to run IGM to generate a population which uses a given combination of data sources, the ```igm-config.json``` file needs to be edited accordingly, by specifying the input files and adding/removing the parameters for each data source when applicable (a detailed description of the different entries that are available is given under ```igm/core/defaults```). Then, software can be run using ```igm-run igm-config.json```. Specifically:
 
 -   Go into ```igm-config.json``` file (or your config file) and edit ```optimization/kernel_opts/lammps/lammps_executable``` so that it points to the actual lammps executable file being installed (see Installation on Linux)
-   If run serially (as a test), go into ```igm-config.json``` (or your config) file and set ```parallel/controller``` to "serial". Then execute IGM (from the command line or by submitting a serial job to HPC cluster) by typing ```igm-run config_file.json >> output.txt```. 
-   If run in parallel (this is for actual calculations), go into ```igm-config.json``` file and set ```parallel/controller``` to "ipyparallel" and then follow the steps detailed in ```HPC_scripts\steps_to_submit_IGM.txt``` file and in the documentation, which rely on scripts also in the ```HPC_scripts``` folder. Specifically: create a running ipcluster environment (```bash create_ipcluster_environment.sh``` followed by ```qsub submit_engines.sh```) and only then submit the actual IGM calculation (```qsub submit_igm.sh```), which executes the ```igm-run igm-config.json``` command, i.e.
 
    ```
    bash create_ipcluster_environment.sh
    qsub submit_engines.sh
    qsub submit_igm.sh
    ```
 
 [Commands and sintax will need to be adapted if different scheduler than SGE is available]
 
-   A successful run should generate a ```igm.log``` and ```stepdb.splite``` files, a number of temporary files from the Assignment Steps and finally  a sequence of intermediate .hss genome populations, each resulting from a different A/M iteration (see ```IGM_documentation.pdf```). The file ```igm-model.hss``` will contain the optimized population at the end of the pipeline. hss files can be read conveniently using the ```alabtools``` package which was mentioned already.
-   A non-successful run (for whatever reason) should produce the ```err_igm``` file with details about the reason why the run crashed. If a run accidentally crashes (like, a node goes down), resubmitting the calculation using ```qsub submit_igm.sh``` (assuming the ipcluster environment is still up and running) will pick up exactly where the previous run left off. However, if a fresh new calculation has to start from the top, please make sure all the temporary files (including the database ```stepdb.splite```) and the ```tmp``` folder are removed before submitting.
 
 
In order to get familiar with the configuration file and  the code execution, we provide a ```config_file.json``` demo configuration file for running a 2Mb resolution WTC11 population using Hi-C data only: that is found in the ```demo``` folder. 

A comprehensive configuration file ```igm-config_all.json``` for running a HFF population with all data types (Hi-C, lamina DamID, SPRITE and 3D HIPMap FISH) is also provided here as a reference/template. Clearly, each user must specify their own input files.
 
 
 Software demo
 ------------
 
 Sample files at provided to simulate a Hi-C only population of WTC11 (spherical nucleus) at 2Mb resolution, to get familiar with the basics of the code
 
-   Enter the ```demo``` folder: data and scripts for a 2Mb IGM calculation with Hi-C restraints are provided;
    -   ```.hcs``` file is a 2Mb resolution Hi-C contact map
    - ``` config_file.json ``` is the .json configuration file with all the parameters needed for the calculation. In particular, we generate 100 structures, which means the lowest contact probability we can target is 0.01 (1 %). For different setups, we recommend using different names for the configuration file to avoid confusion. Whatever name is chosen, it will have to be updated when running the scripts.
    - Run IGM as detailed in the previous section (```igm-run config_file.json```), either serially or in parallel; the serial calculation (on a normal computer) all the way down to 1% probability should be completed in a few hours.

