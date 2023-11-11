FROM quay.io/jupyter/base-notebook
ENV GOOGLE_APPLICATION_CREDENTIALS credentials.json
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"