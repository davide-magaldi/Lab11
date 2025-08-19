from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._product = None

    def fillDD(self):
        colors = self._model.getColors()
        for c in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

    def handle_graph(self, e):
        year = self._view._ddyear.value
        color = self._view._ddcolor.value
        if year is None or color is None:
            self._view.create_alert("Selezionare un anno e un colore!")
            return
        self._view.btn_search.disabled = True
        self._view.update_page()
        time = datetime.now()
        self._model.createGraph(year, color)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()}, Numero di archi: {self._model.getNumEdges()}"))
        for n in self._model.getEdgesMaxWeight():
            self._view.txtOut.controls.append(ft.Text(f"Arco da {n[0].Product_number} a {n[1].Product_number}, peso={self._model._graph.get_edge_data(n[0], n[1])['weight']}"))
        rep = self._model.getRepeatedProducts()
        if len(rep) == 0:
            self._view.txtOut.controls.append(ft.Text("Non ci sono prodotti ripetuti"))
        else:
            self._view.txtOut.controls.append(ft.Text(f"I prodotti ripetuti sono {rep}"))
        self._view.txtOut.controls.append(ft.Text(f"Tempo: {datetime.now()-time}"))
        self.fillDDProduct()
        self._view.update_page()

    def fillDDProduct(self):
        nodes = self._model._graph.nodes
        self._view._ddnode.options.clear()
        for n in nodes:
            self._view._ddnode.options.append(ft.dropdown.Option(key=n.Product_number, data=n, on_click=self.read_data))

    def read_data(self, e):
        self._product = e.control.data
        self._view.btn_search.disabled = False
        self._view.update_page()

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text("Sto cercando il percorso..."))
        self._view.update_page()
        time = datetime.now()
        path = self._model.getMaxPath(self._product, self._model._graph)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Tempo impiegato: {datetime.now()-time}"))
        self._view.txtOut2.controls.append(ft.Text(f"Percorso più lungo con {len(path)-1} archi:"))
        for n in path:
            self._view.txtOut2.controls.append(ft.Text(n.Product_number))
        self._view.update_page()
