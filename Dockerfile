FROM jrottenberg/ffmpeg:8.0-ubuntu2404

WORKDIR /workspace

COPY generate_barcode.sh /generate_barcode.sh
RUN chmod +x /generate_barcode.sh

ENTRYPOINT ["/generate_barcode.sh"]
