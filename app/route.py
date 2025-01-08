from flask import (
    Blueprint, flash,
    redirect, render_template,
    request, send_file, url_for, current_app
)
from werkzeug.utils import secure_filename
from app.forms import CPFForm
from pdf_mod import modifier_pdf
import os


bp = Blueprint('route', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = CPFForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('O Arquivo não foi selecionado', 'danger')
            return redirect(url_for('route.index'))
        file = request.files['file']
        if file.filename == '':
            flash('O Arquivo nao foi selecionado', 'danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            # Acessando a configuração de UPLOAD_FOLDER através do current_app
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            cpf = form.cpf.data
            position = form.position.data
            color = form.color.data
            try:
                # Modifica o PDF e salva com novo nome
                modified_filepath = modifier_pdf(
                    file_path, cpf, position, color, current_app.config['UPLOAD_FOLDER'])
                form.reset()
                # Retorna o arquivo modificado para o usuário
                return send_file(modified_filepath, as_attachment=True)

            except Exception as e:
                flash(
                    f'ERRO: Não foi possível carregar o PDF: {str(e)}', 'danger')
                return redirect(url_for('route.index'))
    return render_template('index.html', form=form)
