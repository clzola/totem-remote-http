# TotemRemoteHttp

Providing HTTP interface for controlling [totem video player](https://wiki.gnome.org/Apps/Videos).
It has web interface at ```http://localhost:9090/interface```. You can find list of API calls bellow.

## Instalation

Download this repository and move the `TotemRemoteHttp` directory to:
```
~/.local/share/totem/plugins/
```
and then you can enable it in ***Edit → Preferences → Plugins***, find ***Totem Remote HTTP***
and tick checkbox.

## Usage

Plugin creates http server and currently listens to port 9090. I am planing to create some sort of window for configuring this port.
There are serveral actions that can be performed.

```
http://localhost:9090/status
```

***Example***

Request:
```
GET http://localhost:9090/status
```

Response:
```
{
    "current_time": 1635054, 
    "display_name": "Exodus.Gods.and.Kings.2014.1080p.3D.HSBS.BluRay.x264.YIFY.mp4", 
    "fullscreen": false, 
    "state": true, 
    "volume": 0.19999694824218753, 
    "stream_length": 9019156
}
```

### API

#### Interface

Shows player API interface for testing.

Route:
```
GET http://[ip_address]:9090/
GET http://[ip_address]:9090/interface
```

#### Status

Retrieves status of currently playing video.

Route:
```
GET http://[ip_address]:9090/staus
```

##### Volume

Sets new volume value.

Route:
```
POST http://[ip_address]:9090/volume/{value}
```

| Parameter |  Type  | Location | Description                |
|-----------|--------|----------|----------------------------|
| value     | float  | route    | Must be between 0 and 1    |

#### Forward

Moves forward through video stream by 60 seconds.

Route:
```
POST http://[ip_address]:9090/forward
```

#### Backward

Moves backward through video stream by 15 seconds.

Route:
```
POST http://[ip_address]:9090/backward
```

#### Seek

Positions at exact location of video stream from beginning.

Route:
```
POST http://[ip_address]:9090/seek/{time}
```

| Parameter |  Type  | Location | Description                |
|-----------|--------|----------|----------------------------|
| time      | long   | route    | Location in video stream in milliseconds from begining of video stream    |

#### Toggle Fullscreen

Toggles fullscreen mode.

Route:
```
POST http://[ip_address]:9090/toggle/fullscreen
```

#### Next Video/Chapter

Play the next playlist item or next chapter.

Route:
```
POST http://[ip_address]:9090/playlist/next
```

#### Previous Video/Chapter

Play the previous playlist item or previous chapter.

Route:
```
POST http://[ip_address]:9090/playlist/previous
```

#### Play/Pause

Toggle play/pause on the current stream.

Route:
```
POST http://[ip_address]:9090/playpause
```

#### Remote

Executes the specified command on instance of Totem.

Route:
```
POST http://[ip_address]:9090/remote/{command}
```

| Parameter |  Type  | Location | Description                |
|-----------|--------|----------|----------------------------|
| command   | string | route    | Name of command            |

Available commands:

- PLAY
- PAUSE
- STOP
- PLAYPAUSE
- NEXT
- PREVIOUS
- SEEK_FORWARD
- SEEK_BACKWARD
- VOLUME_IP
- VOLUME_DOWN
- FULLSCREEN
- QUIT
- ENQUEUE
- REPLACE
- SHOW
- UP
- DOWN
- LEFT
- RIGHT
- SELECT
- DVD_MENU
- ZOOM_UP
- ZOOM_DOWN
- EJECT
- PLAY_DVD
- MUTE
- TOGGLE_ASPECT

