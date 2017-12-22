FROM dockcross/windows-x64:latest

RUN cd /usr/src/mxe \
  && make -j$(nproc) MXE_TARGETS='x86_64-w64-mingw32.static.posix' gcc cmake-conf

ENV CMAKE_TOOLCHAIN_FILE /usr/src/mxe/usr/x86_64-w64-mingw32.static.posix/share/cmake/mxe-conf.cmake
RUN echo 'set(CMAKE_CROSSCOMPILING_EMULATOR "/usr/bin/wine")' >> ${CMAKE_TOOLCHAIN_FILE}
RUN cd /usr/local/bin \
  && rm cmake cpack \
  && ln -s /usr/src/mxe/usr/bin/x86_64-w64-mingw32.static.posix-cmake cmake \
  && ln -s /usr/src/mxe/usr/bin/x86_64-w64-mingw32.static.posix-cpack cpack

ENV CROSS_TRIPLE x86_64-w64-mingw32.static.posix
ENV AS=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-as \
    AR=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-ar \
    CC=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-gcc \
    CPP=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-cpp \
    CXX=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-g++ \
    LD=/usr/src/mxe/usr/bin/${CROSS_TRIPLE}-ld

ENV DEFAULT_DOCKCROSS_IMAGE chemfiles-w64
