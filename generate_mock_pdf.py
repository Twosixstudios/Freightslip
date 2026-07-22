from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def create_mock_rate_con():
    filename = "mock_rate_con_multipage.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        "H2Style",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6,
        bold=True,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    bold_style = ParagraphStyle("BoldStyle", parent=normal_style, bold=True)

    story = []

    # ==================== PAGE 1 ====================
    header_data = [
        [
            Paragraph(
                "<b>APEX FREIGHT SYSTEMS LLC</b><br/>100 Logistics Way, Suite 400<br/>Dallas, TX 75201<br/>Phone: (800) 555-0199",
                normal_style,
            ),
            Paragraph(
                "<b>RATE CONFIRMATION SHEET</b><br/><b>Load / Ref #:</b> APX-99482<br/><b>Date:</b> July 21, 2026<br/><b>Equipment:</b> 53' Dry Van",
                normal_style,
            ),
        ]
    ]
    t_header = Table(header_data, colWidths=[270, 270])
    t_header.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ])
    )
    story.append(t_header)
    story.append(Spacer(1, 15))

    # FINANCIAL SUMMARY
    story.append(Paragraph("FINANCIAL HIGHLIGHTS & PAYLOAD", h2_style))
    fin_data = [
        [
            Paragraph("<b>Line Haul Rate:</b>", normal_style),
            Paragraph("$3,200.00", normal_style),
            Paragraph("<b>Fuel Surcharge (FSC):</b>", normal_style),
            Paragraph("$450.00", normal_style),
        ],
        [
            Paragraph("<b>Stop Off Fee:</b>", normal_style),
            Paragraph("$200.00", normal_style),
            Paragraph(
                "<b>TOTAL CARRIER PAY:</b>",
                ParagraphStyle(
                    "Pay",
                    parent=bold_style,
                    textColor=colors.HexColor("#166534"),
                    fontSize=10,
                ),
            ),
            Paragraph(
                "<b>$3,850.00</b>",
                ParagraphStyle(
                    "PayVal",
                    parent=bold_style,
                    textColor=colors.HexColor("#166534"),
                    fontSize=10,
                ),
            ),
        ],
    ]
    t_fin = Table(fin_data, colWidths=[135, 135, 135, 135])
    t_fin.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(t_fin)
    story.append(Spacer(1, 15))

    # ROUTE & STOPS
    story.append(Paragraph("ROUTE & STOP DETAILS", h2_style))
    route_data = [
        [
            Paragraph("<b>Stop 1 (ORIGIN):</b>", bold_style),
            Paragraph(
                "<b>Apex Logistics Hub</b><br/>1200 Industrial Blvd, Dallas, TX 75201<br/><b>Appt:</b> 07/22/2026 @ 08:00 CST",
                normal_style,
            ),
        ],
        [
            Paragraph("<b>Stop 2 (DESTINATION):</b>", bold_style),
            Paragraph(
                "<b>Pacific Distribution Center</b><br/>8800 Supply Chain Rd, Los Angeles, CA 90001<br/><b>Appt:</b> 07/24/2026 @ 06:00 PST",
                normal_style,
            ),
        ],
    ]
    t_route = Table(route_data, colWidths=[150, 390])
    t_route.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )
    story.append(t_route)
    story.append(Spacer(1, 15))

    # METRICS
    meta_data = [
        [
            Paragraph(
                "<b>Broker Name:</b> Apex Freight Systems LLC", normal_style
            ),
            Paragraph(
                "<b>Commodity:</b> Commercial Electronics", normal_style
            ),
        ],
        [
            Paragraph("<b>Total Miles:</b> 1,435 Miles", normal_style),
            Paragraph("<b>Weight:</b> 38,500 lbs", normal_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([("PADDING", (0, 0), (-1, -1), 4)]))
    story.append(t_meta)

    # ==================== PAGE BREAK ====================
    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    story.append(
        Paragraph("CARRIER TERMS & CONDITIONS (PAGE 2 OF 2)", h2_style)
    )
    terms_text = """
    <b>1. Load Confirmation:</b> By accepting this shipment, Carrier agrees to transport the freight specified herein in accordance with all safety regulations and terms established in the Master Broker-Carrier Agreement.<br/><br/>
    <b>2. Check-In Policy:</b> Driver must report arrival and departure times at all facilities via automated tracking or dispatch call. Failure to maintain active tracking may incur a $100 rate adjustment.<br/><br/>
    <b>3. Detention Pay:</b> $50.00/hour after 2 hours of free time at shipper or receiver, provided driver arrives on time and notifies dispatch prior to free time expiration.<br/><br/>
    <b>4. Proof of Delivery:</b> Signed Bills of Lading (BOL) and delivery receipts must be submitted within 48 hours of delivery to process carrier payment.
    """
    story.append(Paragraph(terms_text, normal_style))
    story.append(Spacer(1, 40))

    # SIGNATURE BLOCK
    sig_data = [
        [
            Paragraph(
                "<b>Dispatch Signature:</b> ___________________________",
                normal_style,
            ),
            Paragraph("<b>Date:</b> ______________", normal_style),
        ],
        [
            Paragraph(
                "<b>Driver Name:</b> ______________________________",
                normal_style,
            ),
            Paragraph(
                "<b>Tractor / Trailer #:</b> ___________", normal_style
            ),
        ],
    ]
    t_sig = Table(sig_data, colWidths=[360, 180])
    t_sig.setStyle(TableStyle([("PADDING", (0, 0), (-1, -1), 10)]))
    story.append(t_sig)

    doc.build(story)


if __name__ == "__main__":
    create_mock_rate_con()
    print("Successfully generated 'mock_rate_con_multipage.pdf'!")