import os, shutil, sys, traceback

def showExceptionAndExit(et, ev, tb): # https://stackoverflow.com/questions/779675/stop-python-from-closing-on-error
    traceback.print_exception(et, ev, tb)
    input("Enter 키로 종료하기: ")
    sys.exit(-1)

def redText(s): # https://pypi.org/project/colorama/가 있지만, 빨간색만 표시해주면 되므로 그 라이브러리를 사용하지 않음. 
    return f"{chr(27)}[91m{s}{chr(27)}[0m"

def readlines(path): # \n을 추가해주는 readlines
    with open(path, 'r') as file:
        lines = file.readlines()
    if len(lines) == 0:
        return ["\n"]
    if lines[-1][-1] != "\n":
        lines[-1] += "\n"
        return lines
    return lines

class Rev: # 단일 수정사항 class
    def __init__(self, lineStart, indentO, pathO, indentM, pathM):
        self.lineStart = lineStart
        self.contentO = list(map(lambda s: " " * indentO + s, readlines("revisions/" + pathO)))
        self.contentM = list(map(lambda s: " " * indentM + s, readlines("revisions/" + pathM)))
        self.lineEnd = self.lineStart + len(self.contentO)

class Revs: # 수정사항 class
    def __init__(self, path, *revlist):
        assert path[0] != "." and os.path.exists(path)
        self.path = path
        self.content = readlines(self.path)
        self.revlist = revlist
        for rev in self.revlist:
            assert isinstance(rev, Rev)
        assert 0 <= self.revlist[0].lineStart
        for i in range(len(self.revlist)-1):
            assert self.revlist[i].lineEnd <= self.revlist[i+1].lineStart
        assert self.revlist[-1].lineEnd <= len(self.content)

    def execute(self):
        result = []
        lineStarts = [rev.lineStart for rev in self.revlist] + [len(self.content)]
        lineEnds   = [0] + [rev.lineEnd for rev in self.revlist]
        for i in range(2*len(self.revlist)+1):
            if i % 2 == 0:
                for j in range(lineEnds[i//2], lineStarts[i//2]):
                    result.append(self.content[j])
            else:
                rev = self.revlist[i//2]
                for j in range(lineStarts[i//2], lineEnds[i//2 + 1]):
                    assert self.content[j] == rev.contentO[j - lineStarts[i//2]]
                result += rev.contentM
        with open(self.path, 'w') as file:
            for res in result:
                file.write(res)

MOD_NAME = "toy_oxMod"
sys.excepthook = showExceptionAndExit

# main
os.system("")
assert os.path.exists("toy.jar"),             redText('"oxModder" 폴더 안에 "toy.jar"를 둬야 합니다. ')
assert not os.path.isdir(MOD_NAME),           redText(f'"oxModder" 폴더 안에 "{MOD_NAME}"라는 다른 폴더가 있으면 안됩니다. ')
assert not os.path.exists(MOD_NAME + ".zip"), redText(f'"oxModder" 폴더 안에 "{MOD_NAME}.zip"라는 다른 파일이 있으면 안됩니다. ')
assert not os.path.exists(MOD_NAME + ".jar"), redText(f'"oxModder" 폴더 안에 "{MOD_NAME}.jar"라는 다른 파일이 있으면 안됩니다. ')
assert shutil.which("javac") is not None,     redText('"javac"가 설치되어 있어야 합니다. ')
shutil.unpack_archive("toy.jar", MOD_NAME, "zip") # unzip
with open(MOD_NAME + "/version", 'r') as versionFile: # check version
    version = versionFile.read()
    assert version == "7.1.649\n12/18/10\n", redText('현재 "oxMod"에서 지원하지 않는 "toy.jar" 버전입니다. ')

# edit java files
TFrame = Revs(MOD_NAME + "/src/edu/princeton/toy/TFrame.java", Rev(1404, 4, "1o.txt", 4, "1m.txt"), Rev(1423, 0, "2o.txt", 8, "2m.txt"))
TMain = Revs(MOD_NAME + "/src/edu/princeton/toy/TMain.java", Rev(164, 12, "3o.txt", 12, "3m.txt"))
TFrame.execute()                     
TMain.execute()

# edit config.xml
with open("revisions/cm.txt", 'w') as file:
    file.write(f"<jar>{MOD_NAME}.jar</jar>\n<outfile>{MOD_NAME}.exe</outfile>")
shutil.copyfile("docs/config_original.xml", "config.xml")
config = Revs("config.xml", Rev(4, 2, "co.txt", 2, "cm.txt"))
config.execute()
os.remove("revisions/cm.txt")

# move image
os.remove(MOD_NAME + "/images/splashBackground.jpg")
shutil.copyfile("images/splashBackground.jpg", MOD_NAME + "/images/splashBackground.jpg")

# compile: Windows에서 makefile을 작동시키기 어려웠기 때문에, makefile의 compile 부분을 참고하여 손으로 명령어를 작성하였음. 
os.chdir(MOD_NAME)
shutil.rmtree("edu")
os.remove("ResourceAnchor.class")
os.system("javac -g -d . -sourcepath src -classpath . -deprecation src/*.java src/edu/princeton/toy/*.java src/edu/princeton/toy/choosers/*.java src/edu/princeton/toy/lang/*.java src/edu/princeton/swing/*.java src/edu/princeton/swing/text/*.java")

# zip
os.chdir("..")
shutil.make_archive(MOD_NAME, "zip", MOD_NAME)
os.rename(MOD_NAME + ".zip", MOD_NAME + ".jar")
shutil.rmtree(MOD_NAME)

print(redText("oxModder.py가 성공적으로 종료되었습니다. "))