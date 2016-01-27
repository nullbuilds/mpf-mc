from kivy.uix.video import Video
from kivy.core.video import Video as CoreVideo

from mc.uix.widget import MpfWidget


class VideoWidget(MpfWidget, Video):
    widget_type_name = 'Video'

    def __init__(self, mc, config, slide, mode=None, priority=None):
        super().__init__(mc=mc, mode=mode, priority=priority, slide=slide,
                         config=config)

        self.video = self.mc.videos[self.config['video']]

        if not self.video.video:
            self.video.load(callback=self._do_video_load)
            # Set it to transparent while it's loading so we don't see a white
            # box on the slide
            self.color = (1,1,1,0)
        else:
            self._do_video_load()

    def __repr__(self):  # pragma: no cover
        try:
            return '<Video name={}, size={}, pos={}>'.format(self.video.name,
                                                             self.size,
                                                             self.pos)
        except AttributeError:
            return '<Video (loading...), size={}, pos={}>'.format(self.size,
                                                                  self.pos)

    def _do_video_load(self, *largs):
        # Overrides a method in the base Kivy Video widget. It's basically
        # copied and pasted from there, with the change that this method pulls
        # the video object from the MPF asset versus loading from a file and
        # it has the extra bit at the end to set the size and position
        if CoreVideo is None:
            raise TypeError("Could not find a video provider to play back "
                            "the video '{}'".format(self.video.file))
        if self._video:
            self._video.stop()
        elif self.video.video:
            self._video = self.video.video
            self._video.volume = self.volume
            self._video.bind(on_load=self._on_load,
                             on_frame=self._on_video_frame,
                             on_eos=self._on_eos)
            if self.state == 'play' or self.play:
                self._video.play()
            self.duration = 1.
            self.position = 0.

            self.state = 'play'
            self.size = (400, 300)
            # set it back to the final transparency / tint
            self.color = (1,1,1,1)