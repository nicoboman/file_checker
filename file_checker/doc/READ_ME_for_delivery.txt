Notes prises dans le cadre de la création d'un utilitaire autoporteur:

- Utilisation de l'utilitaire 'PyInstaller'
- Afin de compiler avec la librairie Pandas:
	* création du fichier ci-dessous (qui n'existait pas de base):
	C:\Users\nicolas\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyInstaller\hooks\hook-pandas.py
	
	* dans ce fichier, écriture de la ligne suivante:
	hiddenimports = ['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.skiplist']

- Génération de l'utilitaire:
	* se positionner dans C:\Users\nicolas\Documents\A6\Python\checkDATDUT\trunk\
	* commande: pyinstaller main.py --onefile
	ou
	* commande: pyinstaller main.spec
	
	-> voir la documentation PyInstaller pour les options. 