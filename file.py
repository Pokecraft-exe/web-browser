from dataclasses import dataclass
import sys

@dataclass
class Meta:
    size: int
    type: str
    name: str
    ext: str
    
class File:
    Data = ""
    Metadata = Meta(0,None,None,None)

    def Update(self):
        self.Metadata = Meta(0, self.Metadata.type, self.Metadata.name, self.Metadata.ext)
        self.Metadata = Meta(sys.getsizeof(self.Metadata) + sys.getsizeof(self.Data), self.Metadata.type, self.Metadata.name, self.Metadata.ext)

    def Read(self):
        return self.Data

    def ReadBytes(self):
        return str.encode(self.Data)

    def Write(self, NewData):
        self.Data = str(NewData)
        self.Update()

    def Append(self, AppendData):
        self.Data = self.Data + str(AppendData)
        self.Update()


def NewFile(Name, extention):
    Newfile = File()
    Newfile.Metadata = Meta(0, "File", str(Name), str(extention))
    return Newfile
    

