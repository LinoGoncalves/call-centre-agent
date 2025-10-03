"""Generate simple architecture diagrams as PNGs for docs/diagrams.

This script uses Pillow (PIL) to draw basic box-and-arrow diagrams.
It creates:
 - docs/diagrams/system_architecture.png
 - docs/diagrams/routing_decision_tree.png
 - docs/diagrams/mlops_pipeline.png

Run: python tools/generate_diagrams.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'diagrams')
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1200, 700
FONT = None
try:
    FONT = ImageFont.truetype("arial.ttf", 14)
except Exception:
    FONT = ImageFont.load_default()

def draw_box(draw, xy, text):
    x1,y1,x2,y2 = xy
    draw.rectangle(xy, outline='black', width=2, fill='#f7f7f7')
    # Measure text size in a Pillow-version-compatible way and support multiline text.
    try:
        # Pillow >= 8.0: ImageDraw has multiline_textbbox / textbbox
        if hasattr(draw, 'multiline_textbbox'):
            bbox = draw.multiline_textbbox((0, 0), text, font=FONT)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            text_x = x1 + (x2 - x1 - w) / 2
            text_y = y1 + (y2 - y1 - h) / 2
            draw.multiline_text((text_x, text_y), text, fill='black', font=FONT, align='center')
        elif hasattr(FONT, 'getbbox'):
            # Fallback: compute bbox per-line
            lines = text.splitlines()
            line_heights = []
            max_w = 0
            for ln in lines:
                bbox = FONT.getbbox(ln)
                lw = bbox[2] - bbox[0]
                lh = bbox[3] - bbox[1]
                max_w = max(max_w, lw)
                line_heights.append(lh)
            total_h = sum(line_heights) + (len(lines)-1) * 4
            text_x = x1 + (x2 - x1 - max_w) / 2
            text_y = y1 + (y2 - y1 - total_h) / 2
            # Draw each line centered
            cur_y = text_y
            for i, ln in enumerate(lines):
                bbox = FONT.getbbox(ln)
                lw = bbox[2] - bbox[0]
                draw.text((x1 + (x2 - x1 - lw) / 2, cur_y), ln, fill='black', font=FONT)
                cur_y += line_heights[i] + 4
        else:
            # Older Pillow: fall back to textsize if available, else approximate
            if hasattr(draw, 'textsize'):
                w,h = draw.textsize(text, font=FONT)
            else:
                # estimate: 7px per character width, 14px per line height
                lines = text.splitlines()
                w = max(len(ln) for ln in lines) * 7
                h = len(lines) * 14
            text_x = x1 + (x2-x1 - w)/2
            text_y = y1 + (y2-y1 - h)/2
            draw.text((text_x, text_y), text, fill='black', font=FONT)
    except Exception:
        # Last-resort: draw top-left aligned
        draw.text((x1+8, y1+8), text, fill='black', font=FONT)

# 1) System architecture
img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
d = ImageDraw.Draw(img)
# Top: Streamlit UI
draw_box(d, (100,50,1100,140), 'Streamlit UI\n(src/ui/streamlit_demo.py)')
# Middle: Orchestrator
draw_box(d, (200,180,1000,300), 'Enhanced Classifier / Orchestrator\n(src/models/enhanced_classifier.py)')
# Bottom left: Traditional ML
draw_box(d, (80,360,420,520), 'Traditional ML\n(src/models/)')
# Bottom right: Gemini LLM
draw_box(d, (780,360,1120,520), 'Gemini LLM (RAG)\n(LLM Provider)')
# Arrows
d.line((600,140,600,180), fill='black', width=3)
d.line((600,300,250,360), fill='black', width=3)
d.polygon([(250,360),(245,352),(255,352)], fill='black')
d.line((600,300,950,360), fill='black', width=3)
d.polygon([(950,360),(945,352),(955,352)], fill='black')
img.save(os.path.join(OUT_DIR, 'system_architecture.png'))

# 2) Routing decision tree
img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
d = ImageDraw.Draw(img)
# Root
draw_box(d, (430,40,770,130), 'Incoming Ticket')
# Rules engine
draw_box(d, (80,190,420,280), 'Rules Engine\n(YAML rules)')
# Vector DB
draw_box(d, (440,190,760,280), 'Vector DB Similarity\n(Pinecone/Qdrant)')
# Traditional ML
draw_box(d, (80,380,420,470), 'Traditional ML Prediction')
# LLM
draw_box(d, (440,380,760,470), 'LLM + RAG (Gemini)')
# Final
draw_box(d, (430,560,770,650), 'Final Routing Decision')
# Connections
d.line((600,130,600,190), fill='black', width=3)
# to rules
d.line((430,130,250,190), fill='black', width=3)
d.polygon([(250,190),(258,188),(255,198)], fill='black')
# to vector
d.line((600,130,600,190), fill='black', width=3)
d.polygon([(600,190),(592,188),(600,198)], fill='black')
# rules -> final (if match)
d.line((250,280,600,560), fill='black', width=3)
d.polygon([(600,560),(593,553),(610,555)], fill='black')
# vector -> ml/llm
d.line((600,280,250,380), fill='black', width=3)
d.polygon([(250,380),(260,375),(260,385)], fill='black')
d.line((600,280,760,380), fill='black', width=3)
d.polygon([(760,380),(752,372),(762,372)], fill='black')
# ml/llm -> final
d.line((250,470,600,560), fill='black', width=3)
d.polygon([(600,560),(593,553),(610,555)], fill='black')
img.save(os.path.join(OUT_DIR, 'routing_decision_tree.png'))

# 3) MLOps pipeline
img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
d = ImageDraw.Draw(img)
# Left: Ingestion
draw_box(d, (50,80,300,160), 'Ticketing Systems\n(ServiceNow/Zendesk)')
# ETL
draw_box(d, (350,80,650,160), 'Ingestion & Sanitization\n(Airflow)')
# Embeddings
draw_box(d, (700,80,1050,160), 'Embedding Generation\n(Embeddings API)')
# Model training
draw_box(d, (200,260,500,360), 'Model Training\n(MLflow + Kubeflow)')
# Model registry
draw_box(d, (600,260,900,360), 'Model Registry\n(MLflow)')
# Serving
draw_box(d, (350,440,850,560), 'Model Serving\n(FastAPI + KServe)')
# Arrows
d.line((300,120,350,120), fill='black', width=3)
d.polygon([(350,120),(342,115),(342,125)], fill='black')

d.line((650,120,700,120), fill='black', width=3)
d.polygon([(700,120),(692,115),(692,125)], fill='black')

d.line((500,310,600,310), fill='black', width=3)
d.polygon([(600,310),(592,305),(592,315)], fill='black')

d.line((750,360,750,440), fill='black', width=3)
d.polygon([(750,440),(742,435),(760,435)], fill='black')

img.save(os.path.join(OUT_DIR, 'mlops_pipeline.png'))

print('Diagrams written to', OUT_DIR)