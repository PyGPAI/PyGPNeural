# PyGPNeural

Neural computations represented in python and OpenCL.

Currently still in development.

## Showcase

### PyGPRetina

The PyGPRetina subtree preforms approximately the same transformations the RGC cells in the human eye do. Effort was made to keep the transforms operating in real time.

#### Checkerboard Illusion

Here, we can see the edge detector succumbing to the checkerboard illusion. Despite that connector being the same color, it says it's brighter than its surroundings when outside of the shadow, and darker than its surroundings when inside the shadow.

![Image of computer succumbing to the checkerboard illusion.](https://thumbs.gfycat.com/MerryVibrantBasilisk-size_restricted.gif)

#### Pac Man Illusion

Here, the time averaging filter is used in addition to the relative color filter so that the pac man filter works just like it would with any human.

![Image of computer succumbing to the pac man illusion.](https://thumbs.gfycat.com/WanWastefulBarnswallow-size_restricted.gif)

The feed of the 'burned in' image from staring at the screen for so long is next:

![Image of pac man illusion with no dot removed.](https://i.imgur.com/Zdpd6Kj.png)

That took a minute or two to build up, so the video feed looked just like that image.

It was weird. I would check back after a while and see a different image, but I couldn't see it changing at all.
