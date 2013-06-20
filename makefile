PORTA = 8000
DOMINIO = '127.0.0.1'

run:
	@echo "instalando os pacotes necessarios"
	pip install -r requirements.txt
	@echo "run -> Aplicacao encurtador $(DOMINIO):$(PORTA)..."
	@export PYTHONPATH=`pwd`:`pwd`/dango_project:$$PYTHONPATH && \
		export DJANGO_SETTINGS_MODULE=encurtador.settings && \
		python encurtador/manage.py syncdb && \
		python encurtador/manage.py runserver $(DOMINIO):$(PORTA)

test:
	@echo "Testando aplicação"
	pip install -r requirements.txt
	@export PYTHONPATH=`pwd`:`pwd`/dango_project:$$PYTHONPATH && \
		export DJANGO_SETTINGS_MODULE=encurtador.settings && \
		python encurtador/manage.py syncdb && \
		python encurtador/manage.py test 
	
