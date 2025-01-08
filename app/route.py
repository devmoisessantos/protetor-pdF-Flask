from flask import (
    Blueprint, flash, redirect,
    render_template, request,
    send_file, url_for, current_app
)
from werkzeug.utils import secure_filename
from app.forms import CPFForm
from app.pdf_mod import modifier_pdf
import os

bp = Blueprint('route', __name__)


def save_file(file):
    """Salva o arquivo enviado e retorna o caminho onde foi salvo."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path


def handle_pdf_modification(file_path, cpf, position, color):
    """Tenta modificar o PDF e retorna o caminho do arquivo modificado."""
    try:
        return modifier_pdf(file_path, cpf, position, color, current_app.config['UPLOAD_FOLDER'])
    except Exception as e:
        raise ValueError(f'Não foi possível carregar o PDF: {str(e)}')


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = CPFForm()

    if form.validate_on_submit():
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('O Arquivo não foi selecionado', 'danger')
            return redirect(request.url)

        # Salva o arquivo e realiza a modificação
        try:
            file_path = save_file(file)
            cpf = form.cpf.data
            position = form.position.data
            color = form.color.data

            modified_filepath = handle_pdf_modification(
                file_path, cpf, position, color)

            # Limpa o formulário após sucesso
            form = CPFForm()

            return send_file(modified_filepath, as_attachment=True)

        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('route.index'))

    return render_template('index.html', form=form)
