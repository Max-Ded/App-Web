import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime
import sqlite3
# définition du nouveau handler

class RequestHandler(http.server.SimpleHTTPRequestHandler):
 # sous-répertoire racine des documents statiques

 # on surcharge la méthode qui traite les requêtes GET
	#def do_POST(self):
		#self.init_params()

		#print(self.path_info[0])

		#if self.path_info[0] == 'service':
		#	response = '<!DOCTYPE html><title>hello</title> <meta charset="utf-8"><p>Bonjour {} {}</p>'.format(self.params['Prenom'][0],self.params['Nom'][0])
		#	self.send(response)
		#else:
			#self.send_error(405)
	static_dir = '/client'

	def do_GET(self):

		self.path = self.static_dir + self.path 

		if self.path[len(self.static_dir):] =='/time':

			now = datetime.now()
			time = now.strftime("Nous sommes le %D à %H:%M:%S")
			response = '<!DOCTYPE html><title>Heure de la machine</title><meta charset="utf-8"><p>{}</p>'.format(time)
			self.send(response)

		if self.path[len(self.static_dir):] =='/countries':

			base = sqlite3.connect(f'{self.static_dir[1:]}/pays.db')
			cursor = base.cursor()
			cursor.execute('SELECT NOM FROM PAYS')
			list_pays = cursor.fetchall()
			response = 'Liste des pays dans la base de données :\n'

			for i,pays in enumerate(list_pays):

				response+=f'[{i}]  - {pays[0]}\n'
			
			response = '<!DOCTYPE html><title>Liste des pays</title><meta charset="utf-8"><pre>' + response + '</pre>'
			self.send(response)
			
		if self.path[len(self.static_dir):len(self.static_dir) + 8] =='/country':

			pays  = self.path[len(self.static_dir) + 9:]
			print(pays)
			base = sqlite3.connect(f'{self.static_dir[1:]}/pays.db')
			cursor = base.cursor()
			cursor.execute('SELECT WP FROM PAYS')
			print(cursor.fetchall())
			cursor.execute('SELECT * FROM PAYS WHERE WP = (?)' , (pays,))

			res = cursor.fetchone()

			if res != None:
				print(res)
				info = f'Nom : {res[0]}\nLongitude : {res[1]}°\nLatitude : {res[2]}°\nCapital : {res[3]}'
				lien = f'<a href = https://fr.wikipedia.org/wiki/' + res[-2] + '> Lien vers la page wikipedia </a>'
				response = f'<!DOCTYPE html><title>Liste des pays</title><meta charset="utf-8"><pre>{info}</pre> <p>{lien}</p>'

				self.send(response)

			else:

				self.send_error(404, 'Ce pays n\'est pas dans la base de donneés')

			cursor.close()

		if self.path[len(self.static_dir):] =='/test':

			print('test')
			text = 'Bonjour\nComment ça va ?\nApproximatively 30 minutes ago i beat the shit out of my dick'
			self.send_response(200)

			self.send_header('Content-Length',int(len(text)))
			self.end_headers()
			text = bytes(text,'utf-8')
			self.wfile.write(text)

		else:

			self.path = self.static_dir + '/index.html'
			print(self.path)
			return http.server.SimpleHTTPRequestHandler.do_GET(self)

	def init_params(self):
	    # analyse de l'adresse    
	    info = urlparse(self.path)
	    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
	    self.query_string = info.query
	    self.params = parse_qs(info.query)
	    # récupération du corps
	    length = self.headers.get('Content-Length')
	    ctype = self.headers.get('Content-Type')
	    if length:
	    	self.body = str(self.rfile.read(int(length)),'utf-8')
	    	if ctype == 'application/x-www-form-urlencoded' :
	    		self.params = parse_qs(self.body)

	def send(self,body):

		encoded = bytes(body, 'UTF-8')

		self.send_response(200)

		self.send_header('Content-Length',int(len(encoded)))
		self.end_headers()
		
		self.wfile.write(encoded)

if __name__ =='__main__':
	# instanciation et lancement du serveur
	httpd = socketserver.TCPServer(("", 8080), RequestHandler)
	httpd.serve_forever()