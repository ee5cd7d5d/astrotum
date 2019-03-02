FROM continuumio/miniconda3
# Add environment
ADD planning_env.yml /tmp/planning_env.yml
RUN conda env create -f /tmp/planning_env.yml
# Pull the environment name out of the yml
RUN echo "source activate $(head -1 /tmp/planning_env.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/planning_env.yml | cut -d' ' -f2)/bin:$PATH

# Install Chrome in the container
USER root
RUN echo "Update"
RUN apt-get update
RUN echo "End Update"
RUN apt-get -y install chromium-browser
RUN echo "Chrome installed"
# drop back to the regular user
USER astronomer


# Run app 
CMD python get_visible_passes.py