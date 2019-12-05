# DLCV_Final_Project
Final Project for Deep Learning for Computer Vision

Resources:

SinGAN Summary 
https://github.com/vlgiitr/papers_we_read/blob/master/summaries/singan.md


Notes:

In each stage, scaling up is approximately 1.23 ~ 1.24, thus 10 upscaling (11 stages) would accumulate to approximately 10x (1.23^11 = 10) ?????

--max_size controls the maximum resolution that the generator sees ?????

harmonization uses dilated mask (for the purpose of incorporating more context ?????)

need to understand Gs, Zs, reals, NoiseAmp and how to substitute them to create different effects (especially NoiseAmp)

500x500 takes 16634 seconds to train with min, max, 50, 500

250x250 orange takes 5121 seconds with min max 25, 250