import os
import subprocess
import commands
import ast

f = open(os.path.join(os.environ["STPOL_DIR"], "datasets", "step2", "mc", "Sep8.sorted"))
for line in f:
    line = line.strip()
    if len(line)>0:
        name, dsname = line.split()
        print dsname
        query = "--query='dataset=" + dsname + " instance=prod/phys03'"
        status, output = commands.getstatusoutput('das_client.py ' +query+ ' --format=json')
        """subprocess.call([
            'das_client.py',
            query
        ])"""
        """output = ast.literal_eval(output)
        print output[0]
        ds = output[0]["dataset"]
        name = output[0]["name"]
        print ds[status], nname["nevents"]"""
        print dsname
        print status
        print output
        print "\n\n\n"

"""
[{"dataset": 
    [{"status": "VALID", 
    "modified_by": "jpata", 
    "physics_group_name": null, 
    "acquisition_era_name": "CRAB", 
    "primary_dataset": {"name": "ZZ_TuneZ2star_8TeV_pythia6_tauola"}, 
    "creation_time": "2014-09-24 18:40:15", 
    "data_tier_name": "USER", 
    "created_by": "jpata", 
    "processed_ds_name": "jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544", 
    "modification_time": "2014-09-24 18:40:15", 
    "datatype": "mc", 
    "xtcrosssection": null, 
    "dataset_id": 316020, 
    "prep_id": null, 
    "processing_version": 1, 
    "name": "/ZZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER"}
    
, {"name": "/ZZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER", 
    "nevents": 2228767, 
    "nlumis": 21444, 
    "nfiles": 200, 
    "nblocks": 1, 
    "size": 549229276545}, 
   {"status": "VALID", "modified_by": "jpata", "physics_group_name": null, "acquisition_era_name": "CRAB", "primary_dataset": {"name": "ZZ_TuneZ2star_8TeV_pythia6_tauola"}, "creation_time": "2014-09-24 18:40:15", "data_tier_name": "USER", "created_by": "jpata", "processed_ds_name": "jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544", "modification_time": "2014-09-24 18:40:15", "datatype": "mc", "xtcrosssection": null, "dataset_id": 316020, "prep_id": null, "processing_version": 1, "name": "/ZZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER"}]
}]
"""

f.close()

#das_client.py --query="dataset=/ZZ_TuneZ2star_8TeV_pythia6_tauola/jpata-Sep8_newjec_metsystshift_hermeticproj-ddf5cfe2d986d6f8e7493e5e618fc544/USER instance=prod/phys03"
