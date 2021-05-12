import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
from PIL import Image
from random import randint, sample

def main():
    k = int(args[0])
    uri = args[1]
    img = None

    if 'http' not in uri:
        img = Image.open(uri)

    width, height = img.size
    pixels = list(img.getdata())
    se = {i for i in pixels}

    # {pixel : number of pixels in image}
    pixel_counts = {}

    for i in pixels:
        if i not in pixel_counts:
            pixel_counts[i] = 1
        else:
            pixel_counts[i] += 1

    most_list = [(pixel_counts[i], i) for i in pixel_counts]
    most = max(most_list)

    print("Size: " + str(width) + " x " + str(height))
    print("Pixels: " + str(len(pixels)))
    print("Distinct pixel count: " + str(len(se)))
    print("Most common pixel: " + str(most[1]) + " => " + str(most[0]))

    indices = sample(range(len(pixels)), k)

    # {index : mean tuple}
    means = {i : pixels[indices[i]] for i in range(k)}

    # {index : {pixel : (number of pixels, distance)}}
    mean_buckets = {i : {} for i in range(k)}

    stop = False
    iterations = 0
    while not stop:
        # print()
        # print("Epoch:", iterations, "-", means)
        iterations += 1
        stop = True

        for pixel in pixel_counts:
            count = pixel_counts[pixel]
            min_distance = None
            best_index = None

            for i in range(k):
                distance = (means[i][0] - pixel[0]) ** 2 + (means[i][1] - pixel[1]) ** 2 + (means[i][2] - pixel[2]) ** 2 

                if min_distance is None or min_distance > distance:
                    min_distance = distance
                    best_index = i

                # if pixel == means[i]:
                #     print("sagdewlkjsldkjfkldsfjklsdjfklsdjfsdlkfjsdfkl")
                #     print(distance)
                #     print(min_distance)
                #     print(means[best_index])
                #     print(pixel in mean_buckets[i])

            if pixel not in mean_buckets[best_index]:
                mean_buckets[best_index][pixel] = (pixel_counts[pixel], min_distance)
                stop = False

            else:
                curr_idx = None
                for j in mean_buckets:
                    if pixel in mean_buckets[j]:
                        curr_idx = j
                        break

                if min_distance < mean_buckets[curr_idx][pixel][1]:
                    mean_buckets[curr_idx].pop(pixel)
                    mean_buckets[best_index][pixel] = (pixel_counts[pixel], min_distance)
                    stop = False

        for i in range(k):
            pixel_sum = [0, 0, 0]
            total_count = 0

            for pixel in mean_buckets[i]:
                count = mean_buckets[i][pixel][0]
                total_count += count

                pixel_sum[0] += pixel[0] * count
                pixel_sum[1] += pixel[1] * count
                pixel_sum[2] += pixel[2] * count
                # print(count)
            
            if total_count != 0:
                new_mean = (pixel_sum[0] / total_count, pixel_sum[1] / total_count, pixel_sum[2] / total_count)
                means[i] = new_mean

            else:
                pass
                # # find the closest mean, make the current mean half the distance towards the closest mean

                # min_dist = None
                # min_mean = None

                # for j in range(k):
                #     distance = (means[j][0] - means[i][0]) ** 2 + (means[j][1] - means[i][1]) ** 2 + (means[j][2] - means[i][2]) ** 2 

                #     if min_dist is None or min_dist > distance:
                #         min_dist = distance
                #         min_mean = j

                # new_mean = ((means[i][0] + means[min_mean][0]) / 2, (means[i][1] + means[min_mean][1]) / 2, (means[i][2] + means[min_mean][2]) / 2)
                # means[i] = new_mean

    # print(means)



    '''
        while not stop:
            stop = True
            for each pixel:
                init min distance and index
                for each index:
                    compare distance w min and find min distance
                if min distance < curr distance:
                    move the pixel to a diff bucket
                    stop = False

            #recompute the means
            for each index:
                init sum and count
                for each pixel:
                    sum[0] += pixel[0], sum[1] += etc
                    count += pixel count

                new pixel mean = (i/count for i in sum)


    '''


    print("Final means:")

    new_pixels = []
    
    for i in means:
        total_pixels = 0
        for pixel in mean_buckets[i]:
            total_pixels += mean_buckets[i][pixel][0]
        print(str(i + 1) + ":", means[i], "=>", total_pixels)

    for i in means:
        means[i] = (int(means[i][0]), int(means[i][1]), int(means[i][2]))

    for p in pixels:
        approx_pixel = None

        for i in means:
            if p in mean_buckets[i]:
                approx_pixel = means[i]
                break
        
        new_pixels.append(approx_pixel)


    final_image = Image.new(img.mode, img.size)
    final_image.putdata(new_pixels)
    final_image.save("kmeans/{}.png".format("2023avasanth"), "PNG")
    

    print("Region counts: 1, 2")




main()