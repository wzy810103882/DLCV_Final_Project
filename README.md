# DLCV_Final_Project
Final Project for Deep Learning for Computer Vision

Resources:

SinGAN Summary https://github.com/vlgiitr/papers_we_read/blob/master/summaries/singan.md


Notes:

In each stage, scaling up is approximately 4/3, thus 8 upscaling would accumulate to approximately 10x ((4/3)^8 = 10)

--max_size controls the maximum resolution that the generator sees

harmonization uses dilated mask (for the purpose of incorporating more context ???)

need to understand Gs, Zs, reals, NoiseAmp and how to substitute them to create different effects (especially NoiseAmp)