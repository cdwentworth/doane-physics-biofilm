'''
 This script is designed to duplicate the MATLAB script of the same name

 Nathan Little
 7/22/13
'''
# Partially Converted
# Assume any strange/nonfunctional code is copied from MATLAB until proven otherwise

def createMovie(movieName,useExisting = 0,docrop = 1):
    """createMovie(movieName,useExisting,docrop)

     This creates a movie by creating the png files from
     the it(*).pov files.

     Set 'useExisting' to 1 to skip creating the image files and
     instead use what was previously rendered

     The docrop argument is optional. If 'docrop' is 0 then
     the images will NOT be cropped. Default value is 1.
    """

    # first create the needed image files
    if !useExisting:
        createPicsNew('all',docrop)

    # now make the movie based on the type of output file

    outtype = movieName(end-2:end);


    if strcmp(outtype,'avi')
            # create the movie using Matlab routines

            iters = getListOfIterates('it','png');
            mov = avifile(movieName);
            for it=1:length(iters)
                    theim = imread(sprintf('it(%04i).png',iters(it)),'BackgroundColor',[1,1,1]);
                    mov = addframe(mov,im2frame(theim));
            
            mov = close(mov);

    else if strcmp(outtype,'gif')
            # create a movie using ImageMagick

            imPATH = getProgramPathNew('ImageMagick');
        dos(sprintf('"%s\\convert.exe" -delay 10 *.png %s',imPATH,movieName));
      
        
    else if strcmp(outtype,'mpg')
            # create a movie using ImageMagick
            imPATH = getProgramPathNew('ImageMagick');
            dos(sprintf('"%s\\convert.exe" -delay 10 *.png %s',imPATH,movieName));

            ## create a movie using ffmpeg
            #ffmpegPATH = getProgramPath('ffmpeg');
            #dos(sprintf('%s\\ffmpeg -v -l -i it(%s).png %s',ffmpegPATH,'%04d',movieName));
