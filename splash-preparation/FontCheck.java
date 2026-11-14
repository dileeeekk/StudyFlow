import java.awt.Font;
import java.awt.font.FontRenderContext;
import java.awt.geom.AffineTransform;
import java.io.File;

class FontCheck {
    public static void main(String[] args) throws Exception {
        var frc = new FontRenderContext(new AffineTransform(), true, true);
        String[] files = {"Inter-Bold.ttf", "Inter-Regular.ttf", "Inter-Medium.ttf"};
        String[] words = {"StudyFlow", "Organize Your Academic Life", "LESS CHAOS. MORE FLOW."};
        float[] sizes = {40, 16, 11};
        for (int i = 0; i < files.length; i++) {
            var font = Font.createFont(Font.TRUETYPE_FONT, new File(args[0], files[i])).deriveFont(sizes[i])
                .deriveFont(java.util.Map.of(java.awt.font.TextAttribute.KERNING, java.awt.font.TextAttribute.KERNING_ON));
            var glyph = font.createGlyphVector(frc, words[i]);
            var lm = font.getLineMetrics(words[i], frc);
            System.out.println(files[i] + " advance=" + font.getStringBounds(words[i], frc).getWidth()
                + " visual=" + glyph.getVisualBounds() + " ascent=" + lm.getAscent() + " descent=" + lm.getDescent());
        }
    }
}
