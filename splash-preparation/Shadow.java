import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

/** Rasterizes only the SVG's Gaussian shadow; the logo itself remains a vector. */
class Shadow {
    public static void main(String[] args) throws Exception {
        final int scale = 3, size = 176 * scale;
        var mask = new BufferedImage(size, size, BufferedImage.TYPE_INT_ARGB);
        var g = mask.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.scale(scale, scale);
        g.translate(0, 12);
        var box = new java.awt.geom.RoundRectangle2D.Double(40, 28, 96, 96, 56, 56);
        g.setColor(new Color(255, 255, 255, 36));
        g.fill(box);
        g.setColor(new Color(255, 255, 255, 102));
        g.setStroke(new BasicStroke(1.5f));
        g.draw(new java.awt.geom.RoundRectangle2D.Double(40.75, 28.75, 94.5, 94.5, 54.5, 54.5));
        // The opaque book contributes to the SVG shadow's alpha mask too.
        var xml = javax.xml.parsers.DocumentBuilderFactory.newInstance().newDocumentBuilder()
            .parse(new File(args[0]));
        String d = ((org.w3c.dom.Element) xml.getElementsByTagName("path").item(0)).getAttribute("d");
        var tokens = java.util.regex.Pattern.compile("[MLVHC]|-?\\d*\\.?\\d+").matcher(d);
        var list = new java.util.ArrayList<String>();
        while (tokens.find()) list.add(tokens.group());
        var path = new java.awt.geom.Path2D.Double();
        double x = 0, y = 0;
        for (int i = 0; i < list.size();) {
            String op = list.get(i++);
            if (op.equals("M") || op.equals("L")) {
                x = Double.parseDouble(list.get(i++)); y = Double.parseDouble(list.get(i++));
                if (op.equals("M")) path.moveTo(x, y); else path.lineTo(x, y);
            } else if (op.equals("V")) {
                y = Double.parseDouble(list.get(i++)); path.lineTo(x, y);
            } else if (op.equals("H")) {
                x = Double.parseDouble(list.get(i++)); path.lineTo(x, y);
            } else if (op.equals("C")) {
                double x1=Double.parseDouble(list.get(i++)), y1=Double.parseDouble(list.get(i++));
                double x2=Double.parseDouble(list.get(i++)), y2=Double.parseDouble(list.get(i++));
                x=Double.parseDouble(list.get(i++)); y=Double.parseDouble(list.get(i++));
                path.curveTo(x1,y1,x2,y2,x,y);
            } else throw new IllegalArgumentException(op);
        }
        g.setColor(Color.WHITE);
        g.setStroke(new BasicStroke(1, BasicStroke.CAP_ROUND, BasicStroke.JOIN_MITER));
        g.draw(path);
        g.dispose();
        int radius = 4 * 20 * scale;
        double[] kernel = new double[2 * radius + 1];
        double sum = 0, sigma = 20 * scale;
        for (int i=-radius; i<=radius; i++) { kernel[i+radius] = Math.exp(-i*i/(2*sigma*sigma)); sum += kernel[i+radius]; }
        for (int i=0; i<kernel.length; i++) kernel[i] /= sum;
        float[] horizontal = new float[size*size];
        for (int y0=0; y0<size; y0++) for (int x0=0; x0<size; x0++) {
            double value=0;
            for (int k=Math.max(-radius,-x0); k<=Math.min(radius,size-1-x0); k++)
                value += (mask.getRGB(x0+k,y0)>>>24)*kernel[k+radius];
            horizontal[y0*size+x0]=(float)value;
        }
        var result = new BufferedImage(size,size,BufferedImage.TYPE_INT_ARGB);
        for (int y0=0; y0<size; y0++) for (int x0=0; x0<size; x0++) {
            double value=0;
            for (int k=Math.max(-radius,-y0); k<=Math.min(radius,size-1-y0); k++)
                value += horizontal[(y0+k)*size+x0]*kernel[k+radius];
            int alpha=(int)Math.round(value*0.25098);
            result.setRGB(x0,y0,(alpha<<24)|0x142869);
        }
        ImageIO.write(result,"png",new File(args[1]));
    }
}
