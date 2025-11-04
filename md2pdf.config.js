module.exports = {
  // Attach custom stylesheet for print-friendly layout
  stylesheet: ['print.css'],

  // Use a readable code highlighting theme
  highlight_style: 'github',

  // Add page size and margins, and simple header/footer with page numbers
  pdf_options: {
    format: 'A4',
    printBackground: true,
    margin: {
      top: '20mm',
      right: '16mm',
      bottom: '20mm',
      left: '16mm'
    },
    displayHeaderFooter: true,
    headerTemplate:
      '<div style="font-size:10px; color:#6b7280; width:100%; text-align:center;">OpenSearch Advanced Workshop</div>',
    footerTemplate:
      '<div style="font-size:10px; color:#6b7280; width:100%; text-align:center;">' +
      '<span class="pageNumber"></span>/<span class="totalPages"></span></div>'
  },

  // Add a class to the body for CSS targeting (optional)
  body_class: 'markdown-body',

  // Ensure Puppeteer can run in restricted environments
  launch_options: {
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
};


