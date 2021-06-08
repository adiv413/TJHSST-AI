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
            
            if total_count != 0:
                new_mean = (pixel_sum[0] / total_count, pixel_sum[1] / total_count, pixel_sum[2] / total_count)
                means[i] = new_mean

            else:
                pass

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
    
    parse_list = [] # stores indices
    region_counts = []
    total_parsed = 0
    curr_region_count = 0
    curr_pixel_mean = None
    next_pixel = None

    while total_parsed < len(new_pixels):
        if len(parse_list) == 0: # either beginning of algorithm or the region is finished
            print(curr_region_count, total_parsed, len(new_pixels))
            if curr_region_count != 0:
                region_counts.append(curr_region_count)
                curr_region_count = 0
            else:
                parse_list.append(0)
                curr_pixel_mean = new_pixels[0]

            # if total_parsed 
            # for i in range(len(new_pixels)): # find the first non "#" thing in the list
            #     if new_pixels[i] != (-1, -1, -1):
            #         print(i)
            #         curr_pixel_mean = new_pixels[i]
            #         parse_list.append(i)
            #         break
            if next_pixel is not None:
                curr_pixel_mean = new_pixels[next_pixel]
                parse_list.append(next_pixel)
                next_pixel = None
            # else:
            #     for i in range(len(new_pixels)): # find the first non "#" thing in the list
            #         if new_pixels[i] != (-1, -1, -1):
            #             print(i)
            #             curr_pixel_mean = new_pixels[i]
            #             parse_list.append(i)
            #             break
        
        if parse_list == []:
            break

        curr_pixel_idx = parse_list.pop()

        if new_pixels[curr_pixel_idx] == curr_pixel_mean:
            # add the recursive cases

            if curr_pixel_idx // width > 0 and new_pixels[curr_pixel_idx - width] == curr_pixel_mean: # go up
                parse_list.append(curr_pixel_idx - width)

            if curr_pixel_idx // width < height - 1 and new_pixels[curr_pixel_idx + width] == curr_pixel_mean: # go down
                parse_list.append(curr_pixel_idx + width)

            if curr_pixel_idx % width > 0 and new_pixels[curr_pixel_idx - 1] == curr_pixel_mean: # go left
                parse_list.append(curr_pixel_idx - 1)

            if curr_pixel_idx % width < width - 1 and new_pixels[curr_pixel_idx + 1] == curr_pixel_mean: # go right
                parse_list.append(curr_pixel_idx + 1)

            if curr_pixel_idx // width > 0 and curr_pixel_idx % width > 0 and new_pixels[curr_pixel_idx - width - 1] == curr_pixel_mean: # go upleft
                parse_list.append(curr_pixel_idx - width - 1)

            if curr_pixel_idx // width > 0 and curr_pixel_idx % width < width - 1 and new_pixels[curr_pixel_idx - width + 1] == curr_pixel_mean: # go upright
                parse_list.append(curr_pixel_idx - width + 1)

            if curr_pixel_idx // width < height - 1 and curr_pixel_idx % width > 0 and new_pixels[curr_pixel_idx + width - 1] == curr_pixel_mean: # go downleft
                parse_list.append(curr_pixel_idx + width - 1)

            if curr_pixel_idx // width < height - 1 and curr_pixel_idx % width < width - 1 and new_pixels[curr_pixel_idx + width + 1] == curr_pixel_mean: # go downright
                parse_list.append(curr_pixel_idx + width + 1)

            # parse current pixel
            new_pixels[curr_pixel_idx] = (-1, -1, -1)
            total_parsed += 1
            curr_region_count += 1

        elif new_pixels[curr_pixel_idx] != (-1, -1, -1):
            print("ooga booga")

        elif next_pixel is None and new_pixels[curr_pixel_idx] != (-1, -1, -1):
            next_pixel = curr_pixel_idx
            print("next", curr_pixel_idx, curr_pixel_mean, new_pixels[next_pixel])

    region_counts.append(curr_region_count)
    print(region_counts)
    print("Region counts: 1, 2")




main()