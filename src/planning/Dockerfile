FROM continuumio/miniconda3
# Add environment
ADD planning_env.yml /tmp/planning_env.yml
RUN conda env create -f /tmp/planning_env.yml
# End stage 0
# Start stage 1
FROM selenium/standalone-chrome
# Copy conda env from stage 1
COPY --from=0 /opt/conda /opt/conda
# Create app
WORKDIR /app
COPY . /app
# Add environment to path
ENV PATH /opt/conda/envs/planning_env/bin:$PATH
EXPOSE 80
ENTRYPOINT ["python", "get_visible_passes.py"]
CMD []