import json
from gi.repository import Totem
from Controllers.BaseController import BaseController

class PlayerController(BaseController):
    def __init__(self, server, request):
        BaseController.__init__(self, server, request)
        self.player = self.server.player
        self.mrl = self.player.get_current_mrl()
        
    def actionStatus(self):        
        self.dumpPlayerStatus()
        
    def actionVolume(self, volume):
        self.player.set_volume(float(volume))
        self.dumpPlayerStatus()
        
    def actionForward(self):
        self.player.remote_command(Totem.RemoteCommand.SEEK_FORWARD, self.mrl)
        self.dumpPlayerStatus()
    
    def actionBackward(self):
        self.player.remote_command(Totem.RemoteCommand.SEEK_BACKWARD, self.mrl)
        self.dumpPlayerStatus()
        
    def actionSeek(self, time):
        self.player.seek_time(int(time), True)
        self.dumpPlayerStatus()
        
    def actionToggleFullscreen(self):
        self.player.remote_command(Totem.RemoteCommand.FULLSCREEN, self.mrl)
        self.dumpPlayerStatus()
        
    def actionNext(self):
        self.player.seek_next()
        self.dumpPlayerStatus()
        
    def actionPrevious(self):
        self.player.seek_previous()
        self.dumpPlayerStatus()
        
    def actionPlayPause(self):
        self.player.play_pause()
        self.dumpPlayerStatus()
    
    def actionStop(self):
        self.player.stop()
        self.dumpPlayerStatus()
        
    def actionRemote(self, command):
        command = Totem.RemoteCommand.__dict__[command]
        self.player.remote_command(command, self.mrl)
        self.dumpPlayerStatus()

    def dumpPlayerStatus(self):
        self.request.send_response(200);
        self.request.send_header('Content-Type', 'application/json')
        self.request.end_headers()
        self.request.wfile.write(bytes(json.dumps(self.getPlayerStatus(), indent=4), 'UTF-8'))
        
    def getPlayerStatus(self):
        status = {
            "current_time": self.player.props.current_time,
            "stream_length": self.player.props.stream_length,
            "state": self.player.props.playing,
            "volume": self.player.get_volume(),
            "display_name": self.player.props.current_display_name,
            "fullscreen": self.player.props.fullscreen
        }
        
        return status
        
        
