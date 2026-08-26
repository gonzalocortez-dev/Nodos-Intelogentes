function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  appendConsulta_(data);
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function appendConsulta_(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Consultas");
  if (!sheet) {
    sheet = ss.insertSheet("Consultas");
  }

  const headers = [
    "Fecha",
    "Nombre",
    "Teléfono / WhatsApp",
    "Email",
    "Ciudad / localidad",
    "Tipo de propiedad",
    "Servicio de interés",
    "Mensaje",
    "Origen",
  ];

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
    sheet.setFrozenRows(1);
  }

  sheet.appendRow([
    data["Fecha"] || "",
    data["Nombre"] || "",
    data["Teléfono / WhatsApp"] || "",
    data["Email"] || "",
    data["Ciudad / localidad"] || "",
    data["Tipo de propiedad"] || "",
    data["Servicio de interés"] || "",
    data["Mensaje"] || "",
    data["Origen"] || "landing",
  ]);
}
