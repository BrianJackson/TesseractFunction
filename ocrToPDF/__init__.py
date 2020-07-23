import logging
import azure.functions as func
import io
import json
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # This assumes a raw binary upload
    try:
        request_body = req.get_body()
        image= Image.open(io.BytesIO(request_body))

    except IOError:
        return func.HttpResponse(
                "Bad input. Unable to cast request body to an image format.",
                status_code=400
        )

    pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
    # pdf is type bytes 
    
    if pdf:
        return func.HttpResponse(body=pdf, mimetype='application/pdf')
    else:
        return func.HttpResponse(
             "Please pass an image in the request body",
             status_code=400
        )
