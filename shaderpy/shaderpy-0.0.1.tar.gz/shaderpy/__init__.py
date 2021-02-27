import pyglet.gl as gl
from ctypes import pointer, cast, create_string_buffer, POINTER, c_char, byref, c_int
import numpy as np
import ctypes

# The Shader class takes as input a list of (path, shader type) tuples


class Shader:

    program = -1
    uniform_locations = {}

    def __init__(self, shader_input):

        shaders = []

        for (path, shader_type) in shader_input:
            source = open(path, "rb").read()
            source_buffer = create_string_buffer(source)
            source_buffer_pointer = cast(pointer(pointer(source_buffer)), POINTER(POINTER(c_char)))
            shader = gl.glCreateShader(shader_type)
            length = c_int(len(source) + 1)
            gl.glShaderSource(shader, 1, source_buffer_pointer, byref(length))
            gl.glCompileShader(shader)

            compile_status = gl.GLint()
            gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, pointer(compile_status))
            if compile_status == gl.GL_FALSE:
                print("Failed to compile shader")

            shaders.append(shader)

        self.program = gl.glCreateProgram()

        for shader in shaders:
            gl.glAttachShader(self.program, shader)

        gl.glLinkProgram(self.program)

        for shader in shaders:
            gl.glDeleteShader(shader)

    def bind(self):
        gl.glUseProgram(self.program)

    def unbind(self):
        gl.glUseProgram(0)

    def delete(self):
        gl.glDeleteProgram(self.program)

    def set_uniform(self, name, v0, v1=None, v2=None, v3=None):
        location = self.__get_uniform_location(name)
        if v3 is not None:
            if isinstance(v0, int):
                gl.glUniform4i(location, v0, v1, v2, v3)
            if isinstance(v0, float):
                gl.glUniform4f(location, v0, v1, v2, v3)
        elif v2 is not None:
            if isinstance(v0, int):
                gl.glUniform3i(location, v0, v1, v2)
            if isinstance(v0, float):
                gl.glUniform3f(location, v0, v1, v2)
        elif v1 is not None:
            if isinstance(v0, int):
                gl.glUniform2i(location, v0, v1)
            if isinstance(v0, float):
                gl.glUniform2f(location, v0, v1)
        else:
            if isinstance(v0, int):
                gl.glUniform1i(location, v0)
            if isinstance(v0, float):
                gl.glUniform1f(location, v0)
            if isinstance(v0, list):
                self.__set_uniform_list(location, v0)

    # The matrix is a list of nested lists. The nested lists are the rows of the matrix.
    def set_uniform_matrix(self, name, matrix, transpose=False):
        location = self.__get_uniform_location(name)
        numpy_matrix = np.array(matrix, gl.GLfloat)
        numpy_matrix_ref = numpy_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        gl.glUniformMatrix4fv(location, 1, transpose, numpy_matrix_ref)

    def __get_uniform_location(self, name):
        if name in self.uniform_locations:
            return self.uniform_locations[name]
        location = gl.glGetUniformLocation(self.program, create_string_buffer(bytes(name, 'utf-8')))
        self.uniform_locations[name] = location
        return location

    def __set_uniform_list(self, location, value):
        if len(value) == 2:
            if isinstance(value[0], float):
                numpy_array = np.array(value, gl.GLfloat)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
                gl.glUniform2fv(location, 1, numpy_array_ref)
            if isinstance(value[0], int):
                numpy_array = np.array(value, gl.GLint)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
                gl.glUniform2iv(location, 1, numpy_array_ref)
        if len(value) == 3:
            if isinstance(value[0], float):
                numpy_array = np.array(value, gl.GLfloat)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
                gl.glUniform3fv(location, 1, numpy_array_ref)
            if isinstance(value[0], int):
                numpy_array = np.array(value, gl.GLint)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
                gl.glUniform3iv(location, 1, numpy_array_ref)
        if len(value) == 4:
            if isinstance(value[0], float):
                numpy_array = np.array(value, gl.GLfloat)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
                gl.glUniform4fv(location, 1, numpy_array_ref)
            if isinstance(value[0], int):
                numpy_array = np.array(value, gl.GLint)
                numpy_array_ref = numpy_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
                gl.glUniform4iv(location, 1, numpy_array_ref)
