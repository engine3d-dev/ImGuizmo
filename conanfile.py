from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy
import os

class ImguizmoRecipe(ConanFile):
    name = "imguizmo"
    version = "1.0"
    package_type = "library"
    license = "Apache-2.0"
    homepage = "https://github.com/engine3d-dev/imgui"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    # exports_sources = "*.h", "*.cpp", "backend/*.h"

    def requirements(self):
        self.requires("make/4.4.1")
        self.tool_requires("cmake/3.27.1")
        self.requires("imguidocking/2.0")

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "*.h", self.recipe_folder, self.export_sources_folder)
        copy(self, "*.cpp", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        # If you use "MinGW Makefiles" on windows, by default looks for mingw32-make.exe instead.
        # Needed to find make.exe installed by choco
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # Copying *.h and *.cpp to a conan/imgui<hash>/p/imguizmo -> *.h
        print(f"[IMGUIZMO] Package Folder = {self.package_folder}\n\n")
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "."))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "ImGuizmo"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "imguizmo::imguizmo")
        self.cpp_info.libs = ["imguizmo"]
        self.cpp_info.includedirs = ['./']  # Ordered list of include paths