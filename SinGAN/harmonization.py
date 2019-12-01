from config import get_arguments
from SinGAN.manipulate import *
from SinGAN.training import *
from SinGAN.imresize import imresize
from SinGAN.imresize import imresize_to_shape
import SinGAN.functions as functions


if __name__ == '__main__':
    parser = get_arguments() # get default parameter (config.py)

    # input image and harmonization mask image
    parser.add_argument('--input_dir', help='input image dir', default='Input/Images') 
    parser.add_argument('--input_name', help='training image name', required=True)
    parser.add_argument('--ref_dir', help='input reference dir', default='Input/Harmonization')
    parser.add_argument('--ref_name', help='reference image name', required=True)

    # inject scale
    parser.add_argument('--harmonization_start_scale', help='harmonization injection scale', type=int, required=True)

    # other options for mode ????
    parser.add_argument('--mode', help='task to be done', default='harmonization')


    opt = parser.parse_args()
    opt = functions.post_config(opt) # some init set opt 


    Gs = []
    Zs = []
    reals = []
    NoiseAmp = []
    dir2save = functions.generate_dir2save(opt) # harmonization img save dir


    if dir2save is None:
        print('task does not exist')
    #elif (os.path.exists(dir2save)):
    #    print("output already exist")
    else: # have valid save directory
        if (os.path.exists(dir2save)):
            print("WARNING: outputs may already exist and they will be overwritten")
        try:
            os.makedirs(dir2save)
        except OSError:
            pass

        real = functions.read_image(opt)
        print("original shape of real: " + ",".join(real.shape))
        #print(real.shape)
        real = functions.adjust_scales2image(real, opt)
        print("adjusted shape of real: " + ",".join(real.shape))
        #print(real.shape)

        Gs, Zs, reals, NoiseAmp = functions.load_trained_pyramid(opt) # load a bunch of trained G, D and etc

        if (opt.harmonization_start_scale < 1) | (opt.harmonization_start_scale > (len(Gs)-1)): # check valid injection scale
            print("injection scale should be between 1 and %d" % (len(Gs)-1))

        else:
            # load naively composite image and mask image
            ref = functions.read_image_dir('%s/%s' % (opt.ref_dir, opt.ref_name), opt) 
            print("ref shape: " + ",".join(ref.shape))
            mask = functions.read_image_dir('%s/%s_mask%s' % (opt.ref_dir,opt.ref_name[:-4],opt.ref_name[-4:]), opt)
            print("mask shape: " + ",".join(mask.shape))

            # some weird shape checking here
            if ref.shape[3] != real.shape[3]:
                print("ref and real different on 4th dimension")
                mask = imresize_to_shape(mask, [real.shape[2], real.shape[3]], opt)
                mask = mask[:, :, :real.shape[2], :real.shape[3]]
                ref = imresize_to_shape(ref, [real.shape[2], real.shape[3]], opt)
                ref = ref[:, :, :real.shape[2], :real.shape[3]]

            mask = functions.dilate_mask(mask, opt) # dilate the binary mask and save it 
            print("mask shape after dilation: " + ",".join(mask.shape))

            N = len(reals) - 1  # total stages
            n = opt.harmonization_start_scale # start injection scale

            # resize ref according to injection scale
            in_s = imresize(ref, pow(opt.scale_factor, (N - n + 1)), opt)
            in_s = in_s[:, :, :reals[n - 1].shape[2], :reals[n - 1].shape[3]]
            in_s = imresize(in_s, 1 / opt.scale_factor, opt)
            in_s = in_s[:, :, :reals[n].shape[2], :reals[n].shape[3]]

            # go through all generators
            out = SinGAN_generate(Gs[n:], Zs[n:], reals, NoiseAmp[n:], opt, in_s, n=n, num_samples=1)
            # real excluding mask + masked output
            # (using dilated mask to enlarge mask and to incorporate more context ???)
            out = (1-mask)*real + mask*out

            # save output
            plt.imsave('%s/start_scale=%d.png' % (dir2save,opt.harmonization_start_scale), functions.convert_image_np(out.detach()), vmin=0, vmax=1)




