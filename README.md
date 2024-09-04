# ICR-Warehouse-routing-optimization

This repository contains my thesis developed to obtain my master in logistics and transportation. It uses mixed optimization through a GRASP algorithm to find a better routing path for multiple orders of items to be manually picked and packed inside a distribution center in Bogotá, Colombia.

The file tiempos_extendidos_reales2.xlsx contains the base necessary to create the movement-times matrix, which is created by CalculadorTiempos Extendidos2.py.

The output file from this is Tiempos_Desplazamiento_CEDI_Reales.xlsx, which then becomes the input along with PLANTILLA PEDIDOS1.xlsx for the file Mejora de rutas 4.py, which contains the preprocessing of data, data organization and GRASP algorithm along with an additional extra step which apllies the GRASP to consolidated routes of small orders, thus increasing efficiency.

This project helped the distribution center (CEDI) reduce movement times by up to 50%, and this resulted in the elimination of approximately 80% of the overtime the company was incurring in.
