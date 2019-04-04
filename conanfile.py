from conans import ConanFile, CMake

class BuildEnvConan(ConanFile):
    build_requires = 'OpenSSL/1.1.1b@conan/stable', 'zlib/1.2.11@conan/stable', 'gtest/1.7.0@bincrafters/stable'
    options = {'static_linking': [True, False, 'auto', 'default']}
    default_options = {'static_linking': 'auto', 'OpenSSL:no_threads': True}
    generators = 'cmake'
    settings = 'build_type'

    def config_options(self):
        if self.options.static_linking == 'auto':
            if self.settings.build_type == "Release":
                self.options['OpenSSL'].shared = False
        elif self.options.static_linking != 'default':
            self.options['gtest'].shared = not self.options.static_linking
            self.options['OpenSSL'].shared = not self.options.static_linking

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")

    def build(self):
        cmake = CMake(self)
        if cmake.generator == 'Unix Makefiles':
            config_args = None
        else:
            config_args = ['-A', 'x64']
        cmake.definitions["OPTIMISE_BUILD"] = self.settings.build_type == "Release"
        cmake.configure(args=config_args)
        cmake.build()
        cmake.test(target='tests')

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
