from pathlib import Path
import xml.etree.ElementTree as ET
import json, hashlib, re

ROOT = Path(__file__).resolve().parent
PROJECT = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
RES = PROJECT / 'app/src/main/res'
A = 'http://schemas.android.com/apk/res/android'
source = ET.parse(RES/'drawable/ic_studyflow_logo.xml').getroot()
path = source.findall('path')[-1].get('{'+A+'}pathData')
out = ROOT/'res'

def write(rel, body):
    p = out/rel
    p.parent.mkdir(parents=True, exist_ok=True)
    ET.fromstring(body)
    p.write_text('<?xml version="1.0" encoding="utf-8"?>\n'+body+'\n', encoding='utf-8')

def book(scale):
    return f'''<group android:translateX="{54-88*scale:.3f}" android:translateY="{54-76*scale:.3f}" android:scaleX="{scale}" android:scaleY="{scale}">
        <path android:pathData="{path}" android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>'''

def gradient(shape):
    return f'''<path android:pathData="{shape}">
        <aapt:attr name="android:fillColor">
            <gradient android:type="linear" android:startX="0" android:startY="0" android:endX="108" android:endY="108">
                <item android:offset="0" android:color="#273D86" />
                <item android:offset="0.55" android:color="#4969E8" />
                <item android:offset="1" android:color="#9672D6" />
            </gradient>
        </aapt:attr>
    </path>'''

def vector(body):
    return f'''<vector xmlns:android="{A}" xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    {body}
</vector>'''

write('drawable/ic_launcher_foreground.xml', vector(book(1.2)))
write('drawable/ic_launcher_background.xml', vector(gradient('M0,0 H108 V108 H0 Z')))
write('mipmap-anydpi/ic_launcher.xml', vector(gradient('M27,3 H81 Q105,3 105,27 V81 Q105,105 81,105 H27 Q3,105 3,81 V27 Q3,3 27,3 Z')+book(1.6)))
write('mipmap-anydpi/ic_launcher_round.xml', vector(gradient('M54,3 A51,51 0,1 1,54,105 A51,51 0,1 1,54,3 Z')+book(1.6)))

before = {str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in RES.rglob('*') if p.is_file()}
assert not (ROOT/'before.json').exists()
(ROOT/'before.json').write_text(json.dumps(before, indent=2), encoding='utf-8')

# Render the original vector path with Java2D; no external packages are required.
tokens = re.findall(r'[MLCHVZmlchvz]|-?\d*\.?\d+', path)
i=0; x=y=0; commands=[]
while i<len(tokens):
    cmd=tokens[i]; i+=1
    count={'M':2,'L':2,'C':6,'H':1,'V':1}[cmd]
    n=list(map(float,tokens[i:i+count]));i+=count
    if cmd=='H': x=n[0]; commands.append(f'p.lineTo({x},{y});')
    elif cmd=='V': y=n[0]; commands.append(f'p.lineTo({x},{y});')
    else:
        x,y=n[-2:]
        method={'M':'moveTo','L':'lineTo','C':'curveTo'}[cmd]
        commands.append('p.'+method+'('+','.join(map(str,n))+');')
java='''import java.awt.*; import java.awt.geom.*; import java.awt.image.*; import javax.imageio.ImageIO; import java.io.*;
public class Preview {
 public static void main(String[] args) throws Exception {
  BufferedImage img=new BufferedImage(1024,512,BufferedImage.TYPE_INT_ARGB);
  Graphics2D g=img.createGraphics(); g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
  g.setColor(new Color(245,247,252)); g.fillRect(0,0,1024,512);
  Path2D p=new Path2D.Double(); COMMANDS
  for(int j=0;j<2;j++) {
   Graphics2D c=(Graphics2D)g.create(); c.translate(80+j*480,64); c.scale(360.0/72,360.0/72); c.translate(-18,-18);
   Shape mask=j==0?new RoundRectangle2D.Double(18,18,72,72,28,28):new Ellipse2D.Double(18,18,72,72);
   c.clip(mask); c.setPaint(new LinearGradientPaint(0,0,108,108,new float[]{0,.55f,1},new Color[]{new Color(0x273D86),new Color(0x4969E8),new Color(0x9672D6)})); c.fillRect(0,0,108,108);
   c.translate(-51.6,-37.2); c.scale(1.2,1.2); c.setColor(Color.WHITE);c.setStroke(new BasicStroke(1,BasicStroke.CAP_ROUND,BasicStroke.JOIN_ROUND));c.draw(p);c.dispose();
  }
  g.dispose();ImageIO.write(img,"png",new File(args[0]));
 }
}'''.replace('COMMANDS','\n'.join(commands))
(ROOT/'Preview.java').write_text(java, encoding='utf-8')
print('Prepared four XML resources and preview renderer.')
