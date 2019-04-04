FROM alpine:3.8

WORKDIR /app
ENV CONAN_USER_HOME=/conan

# Install a base build environment
RUN apk add --no-cache cmake make git python3 python3-dev musl-dev bash g++ perl linux-headers
RUN pip3 install --upgrade pip
RUN pip3 install conan

# Install and Configure conan (forcing C++11 onwards)
RUN mkdir ${CONAN_USER_HOME}
RUN conan profile new default --detect
RUN conan profile update settings.build_type=Release default
RUN conan profile update settings.compiler.libcxx=libstdc++11 default

# Build and install dependencies
COPY ./conanfile.py /app/
RUN conan install /app --build=missing -o static_linking=True
