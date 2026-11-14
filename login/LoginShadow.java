import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

/** Exact SVG button silhouette, offset, color and Gaussian blur at 3x. */
class LoginShadow {
    public static void main(String[] args) throws Exception {
        int scale=3, w=(Integer.parseInt(args[1])+40)*scale, h=(Integer.parseInt(args[2])+40)*scale, radius=40*scale;
        double sigma=10*scale, sum=0;
        var mask=new BufferedImage(w,h,BufferedImage.TYPE_INT_ARGB);
        var g=mask.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
        g.scale(scale,scale);
        g.setColor(Color.WHITE);
        g.fill(new java.awt.geom.RoundRectangle2D.Double(20,20,Integer.parseInt(args[1]),Integer.parseInt(args[2]),Integer.parseInt(args[3])*2,Integer.parseInt(args[3])*2));
        g.dispose();
        double[] kernel=new double[radius*2+1];
        for(int i=-radius;i<=radius;i++){kernel[i+radius]=Math.exp(-i*i/(2*sigma*sigma));sum+=kernel[i+radius];}
        for(int i=0;i<kernel.length;i++)kernel[i]/=sum;
        float[] row=new float[w*h];
        for(int y=0;y<h;y++)for(int x=0;x<w;x++){
            double a=0;
            for(int k=Math.max(-radius,-x);k<=Math.min(radius,w-1-x);k++)a+=(mask.getRGB(x+k,y)>>>24)*kernel[k+radius];
            row[y*w+x]=(float)a;
        }
        var result=new BufferedImage(w,h,BufferedImage.TYPE_INT_ARGB);
        for(int y=0;y<h;y++)for(int x=0;x<w;x++){
            double a=0;
            for(int k=Math.max(-radius,-y);k<=Math.min(radius,h-1-y);k++)a+=row[(y+k)*w+x]*kernel[k+radius];
            result.setRGB(x,y,((int)Math.round(a*Double.parseDouble(args[4]))<<24)|Integer.parseInt(args[5],16));
        }
        ImageIO.write(result,"png",new File(args[0]));
    }
}

