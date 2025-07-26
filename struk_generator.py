from fpdf import FPDF
import datetime
import tempfile
import webbrowser
import os

def buat_struk_pdf(items, total, bayar, kembalian, dp=0):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ARJUNA FOTOCOPY", ln=1, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"Tanggal: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=1)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(10, 8, "No", border=1, align="C")
    pdf.cell(80, 8, "Jenis Layanan", border=1, align="C")
    pdf.cell(20, 8, "Jumlah", border=1, align="C")
    pdf.cell(30, 8, "Harga", border=1, align="C")
    pdf.cell(40, 8, "Subtotal", border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    for i, item in enumerate(items, 1):
        layanan, qty, harga, subtotal = item
        pdf.cell(10, 8, str(i), border=1, align="C")
        pdf.cell(80, 8, layanan, border=1)
        pdf.cell(20, 8, str(qty), border=1, align="C")
        pdf.cell(30, 8, f"Rp{harga:,}", border=1, align="R")
        pdf.cell(40, 8, f"Rp{subtotal:,}", border=1, align="R")
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total     : Rp{total:,}", ln=1, align="R")
    pdf.cell(0, 10, f"Panjar    : Rp{dp:,}", ln=1, align="R")
    pdf.cell(0, 10, f"Bayar     : Rp{bayar:,}", ln=1, align="R")
    pdf.cell(0, 10, f"Kembalian : Rp{kembalian:,}", ln=1, align="R")

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Terima Kasih Atas Kepercayaan Anda!", ln=1, align="C")
    pdf.cell(0, 8, "By : Arjuna Fotocopy", ln=1, align="C")

    # Simpan ke file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        nama_file = tmpfile.name
        pdf.output(nama_file)

    # Buka file PDF di browser default
    webbrowser.open(f"file://{os.path.abspath(nama_file)}")
