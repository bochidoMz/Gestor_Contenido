from flask import Blueprint, render_template, request, redirect, url_for
import Conexion.config as db

manager_perfil = Blueprint('managerPerfil', __name__)

