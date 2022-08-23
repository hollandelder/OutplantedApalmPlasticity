# To run this: paste the path to your main directory containing subdirectories which contain your photos
# (Must have one subdirectory for each coral to be modeled)
# To run in metashape go to tools -> run script -> paste path to script.
# need "r" before the path so it ignores the special functions of \.

# Path deals with windows versus linux issues, so the weird C: and \ won't give you trouble
from pathlib import Path

import os
import Metashape

# This function will take all JPGs in your directory and processes them in Metashape
def processdir(dir):
    os.chdir(dir)
    # line below converts jpg paths to absolute path strings which are needed by addPhotos
    jpgs = [jpg.name for jpg in dir.glob('*.JPG')]
    print(f'''processing {dir.name}
{len(jpgs)} # JPG files
''')
    doc = Metashape.app.document
    chunk = Metashape.app.document.addChunk()
    # NOTE: f strings only work in Python version 3.4 and up
    doc.save(f'{dir.parent.name}_{dir.name}.psz')
    # names the output by the last 2 names in the cwd string, change this to what will properly name the output models
    chunk = doc.chunk
    chunk.addPhotos(jpgs)
    chunk.matchPhotos(downscale=1, generic_preselection=True, keypoint_limit=40000,
                      tiepoint_limit=4000)  # chooses the aligning photos accuracy
    chunk.alignCameras(adaptive_fitting=True)  # function to align photos
    chunk.buildDepthMaps(downscale=4,
                         filter_mode=Metashape.MildFiltering)  # builds high quality dense cloud, ability to change quality and depth filtering (best to keep it at "MILD" for the coral images)
    chunk.buildDenseCloud(point_colors=True)
    chunk.buildModel(surface_type=Metashape.Arbitrary, source=Metashape.DenseCloudData,
                     interpolation=Metashape.EnabledInterpolation,
                     face_count=Metashape.HighFaceCount)  # the "build mesh" step,
    chunk.buildUV(mapping_mode=Metashape.GenericMapping)  # part of build texture step
    chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=25000, fill_holes=True)  # rest of build texture step
    chunk.exportModel(f"{dir.parent.name}_{dir.name}.obj", binary=True, precision=6,
                      texture_format=Metashape.ImageFormatJPEG, texture=True, normals=True, colors=True, cameras=True,
                      markers=True, udim=False, strip_extensions=False, format=Metashape.ModelFormatOBJ)
    doc.save()

# This function will take a directory
def run(dir):
    maindir = Path(dir)
    for x in maindir.glob("*"):
        if x.is_dir():
            processdir(x)
            return

# This prints all paths to your subdirectories full of photos for each samples.
# CHANGE THE DIRECTORY BELOW TO YOUR MAIN DIRECTORY CONTAINING YOUR SUBDIRECTORIES.
if __name__ == "__main__":
    run(r'C:\Users\User\OneDrive\Documents\UniversitySouthernCa\CoralProjects\Apalm_TimeCourse\ApalmPhotoEnvironData\ApalmPhotos\T24_April2020')