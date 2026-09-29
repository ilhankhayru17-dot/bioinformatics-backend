\# Bioinformatics Backend



Backend untuk aplikasi pengolahan dan analisis data sekuens biologis.



\## Features



\- Upload file FASTA/FASTQ

\- Validasi format file

\- Analisis statistik sequence

\- Perhitungan:

&#x20; - jumlah sequence

&#x20; - total panjang sequence

&#x20; - minimum panjang sequence

&#x20; - maksimum panjang sequence

&#x20; - rata-rata panjang sequence

&#x20; - GC percentage

\- Output JSON

\- Output TSV

\- API documentation menggunakan Swagger



\## Project Structure



```text

backend/

├── app/

│   ├── main.py

│   ├── routers/

│   │   ├── upload.py

│   │   └── analysis.py

│   └── services/

│       ├── validation.py

│       └── statistics.py

├── uploads/

├── results/

├── tests/

│   ├── test\_api.py

│   └── test\_statistics.py

├── requirements.txt

├── README.md

└── .gitignore

