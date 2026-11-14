import java.awt.*; import java.awt.geom.*; import java.awt.image.*; import javax.imageio.ImageIO; import java.io.*;
public class Preview {
 public static void main(String[] args) throws Exception {
  BufferedImage img=new BufferedImage(1024,512,BufferedImage.TYPE_INT_ARGB);
  Graphics2D g=img.createGraphics(); g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
  g.setColor(new Color(245,247,252)); g.fillRect(0,0,1024,512);
  Path2D p=new Path2D.Double(); p.moveTo(87.9996,94.0);
p.lineTo(87.9996,66.0);
p.moveTo(87.9996,94.0);
p.curveTo(87.9996,92.4087,87.3675,90.8826,86.2421,89.7574);
p.curveTo(85.1168,88.6321,83.5906,88.0,81.9992,88.0);
p.lineTo(69.9982,88.0);
p.curveTo(69.4677,88.0,68.959,87.7893,68.5839,87.4142);
p.curveTo(68.2088,87.0391,67.998,86.5304,67.998,86.0);
p.lineTo(67.998,60.0);
p.curveTo(67.998,59.4696,68.2088,58.9609,68.5839,58.5858);
p.curveTo(68.959,58.2107,69.4677,58.0,69.9982,58.0);
p.lineTo(79.999,58.0);
p.curveTo(82.1209,58.0,84.1559,58.8429,85.6563,60.3431);
p.curveTo(87.1567,61.8434,87.9996,63.8783,87.9996,66.0);
p.moveTo(87.9996,94.0);
p.curveTo(87.9996,92.4087,88.6318,90.8826,89.7571,89.7574);
p.curveTo(90.8825,88.6321,92.4087,88.0,94.0001,88.0);
p.lineTo(106.001,88.0);
p.curveTo(106.532,88.0,107.04,87.7893,107.415,87.4142);
p.curveTo(107.791,87.0391,108.001,86.5304,108.001,86.0);
p.lineTo(108.001,83.4);
p.moveTo(87.9996,66.0);
p.curveTo(87.9996,63.8783,88.8426,61.8434,90.343,60.3431);
p.curveTo(91.8434,58.8429,93.8784,58.0,96.0003,58.0);
p.lineTo(106.001,58.0);
p.curveTo(106.532,58.0,107.04,58.2107,107.415,58.5858);
p.curveTo(107.791,58.9609,108.001,59.4696,108.001,60.0);
p.lineTo(108.001,64.0);
p.moveTo(96.0003,76.0);
p.lineTo(100.001,80.0);
p.lineTo(108.001,72.0);
  for(int j=0;j<2;j++) {
   Graphics2D c=(Graphics2D)g.create(); c.translate(80+j*480,64); c.scale(360.0/72,360.0/72); c.translate(-18,-18);
   Shape mask=j==0?new RoundRectangle2D.Double(18,18,72,72,28,28):new Ellipse2D.Double(18,18,72,72);
   c.clip(mask); c.setPaint(new LinearGradientPaint(0,0,108,108,new float[]{0,.55f,1},new Color[]{new Color(0x273D86),new Color(0x4969E8),new Color(0x9672D6)})); c.fillRect(0,0,108,108);
   c.translate(-51.6,-37.2); c.scale(1.2,1.2); c.setColor(Color.WHITE);c.setStroke(new BasicStroke(1,BasicStroke.CAP_ROUND,BasicStroke.JOIN_ROUND));c.draw(p);c.dispose();
  }
  g.dispose();ImageIO.write(img,"png",new File(args[0]));
 }
}