from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy
import os

class ImGuizmoRecipe(ConanFile):
    name = "imguizmo"
    version = "1.0"
    package_type = "library"
    license = "Apache-2.0"
    homepage = "https://github.com/engine3d-dev/ImGuizmo"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    # exports_sources = ["CMakeLists.txt", "imconfig.h", "imgui_internal.h", "imgui.h", "imstb_rectpack.h", "imstb_textedit.h", "imstb_truetype.h", "backend/imgui_impl_opengl3.h", "backends/imgui_impl_glfw.h", "backends/imgui_impl_glut.h", "backends/imgui_impl_vulkan.h", "backends/imgui_impl_win32.h"]
    exports_sources = "CMakeLists.txt", "*.h", "*.cpp"

    def requirements(self):
        self.requires("make/4.4.1")
        self.tool_requires("cmake/3.27.1")
        self.requires("glfw/3.4", transitive_headers=True)
        self.requires("opengl/system", transitive_headers=True)
        self.requires("vulkan-loader/1.3.290.0")
        self.requires("imguidocking/1.0")

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
        tc = CMakeToolchain(self, generator="Unix Makefiles")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure()
        cmake.build()

    def package(self):
        # Copying *.h and *.cpp to a conan/imgui<hash>/p/imgui -> *.h
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "."))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "ImGuizmo"))
        copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "."), dst=os.path.join(self.package_folder, "ImGuizmo"))
        # copy(self, pattern="*.h", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_glfw.h", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        # copy(self, pattern="backends/imgui_impl_glfw.cpp", src=os.path.join(self.source_folder, "./backends/"), dst=os.path.join(self.package_folder, "imgui/backends"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "imguizmo::imguizmo")
        # self.cpp_info.libs = ["imguidocking"]
        self.cpp_info.system_libs = ["imguidocking"]
        self.cpp_info.includedirs = ['./']  # Ordered list of include paths
