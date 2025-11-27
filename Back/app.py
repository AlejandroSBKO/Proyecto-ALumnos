import webbrowser
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase_conn import supabase

app = Flask(__name__, static_folder="../Front", static_url_path="", template_folder="../Front")
CORS(app)

@app.route("/")
def home():
    return app.send_static_file("index.html")

def abrir_navegador():
    webbrowser.open_new("http://127.0.0.1:5000")

# =========================
#      RUTAS ALUMNOS
# =========================

# Obtener alumnos de un grupo
@app.route("/api/alumnos/<int:id_grupo>", methods=["GET"])
def get_alumnos(id_grupo):
    try:
        result = supabase.table("alumnos").select("*").eq("id_grupo", id_grupo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crear alumno
@app.route("/api/alumnos", methods=["POST"])
def crear_alumno():
    data = request.json
    try:
        result = supabase.table("alumnos").insert({
            "nombre": data["nombre"],
            "matricula": data.get("matricula", None),
            "id_grupo": data["id_grupo"]
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Editar alumno
@app.route("/api/alumnos/<int:id_alumno>", methods=["PUT"])
def editar_alumno(id_alumno):
    data = request.json
    try:
        result = supabase.table("alumnos").update({
            "nombre": data.get("nombre"),
            "matricula": data.get("matricula"),
        }).eq("id_alumno", id_alumno).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar alumno
@app.route("/api/alumnos/<int:id_alumno>", methods=["DELETE"])
def eliminar_alumno(id_alumno):
    try:
        result = supabase.table("alumnos").delete().eq("id_alumno", id_alumno).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#        RUTAS GRUPOS
# =========================

# Obtener todos los grupos
@app.route("/api/grupos", methods=["GET"])
def obtener_grupos():
    try:
        result = supabase.table("grupos").select("*").execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener un grupo por ID
@app.route("/api/grupos/<int:id_grupo>", methods=["GET"])
def obtener_grupo(id_grupo):
    try:
        result = supabase.table("grupos").select("*").eq("id_grupo", id_grupo).execute()
        if not result.data:
            return jsonify({"error": "Grupo no encontrado"}), 404
        return jsonify(result.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crear grupo
@app.route("/api/grupos", methods=["POST"])
def crear_grupo():
    data = request.json
    try:
        result = supabase.table("grupos").insert({
            "numero": data["numero"],
            "materia": data["materia"]
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Editar grupo
@app.route("/api/grupos/<int:id_grupo>", methods=["PUT"])
def editar_grupo(id_grupo):
    data = request.json
    try:
        result = supabase.table("grupos").update({
            "numero": data.get("numero"),
            "materia": data.get("materia")
        }).eq("id_grupo", id_grupo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar grupo
@app.route("/api/grupos/<int:id_grupo>", methods=["DELETE"])
def eliminar_grupo(id_grupo):
    try:
        result = supabase.table("grupos").delete().eq("id_grupo", id_grupo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# =========================
#   RUTAS UNIDADES
# =========================


@app.route("/api/unidades/<int:id_grupo>", methods=["GET"]) 
def get_unidades(id_grupo):
    try:
        result = supabase.table("unidades").select("*").eq("id_grupo", id_grupo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unidades", methods=["POST"])
def crear_unidad():
    data = request.json
    try:
        result = supabase.table("unidades").insert({
            "numero_unidad": data["numero_unidad"],
            "descripcion": data.get("descripcion", None),
            "id_grupo": data["id_grupo"]
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unidades/<int:id_unidad>", methods=["PUT"])
def editar_unidad(id_unidad):
    data = request.json
    try:
        result = supabase.table("unidades").update({
            "numero_unidad": data.get("numero_unidad"),
            "descripcion": data.get("descripcion")
        }).eq("id_unidad", id_unidad).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unidades/<int:id_unidad>", methods=["DELETE"])
def eliminar_unidad(id_unidad):
    try:
        result = supabase.table("unidades").delete().eq("id_unidad", id_unidad).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#   RUTAS EQUIPOS
# =========================


@app.route("/api/equipos/<int:id_unidad>", methods=["GET"])
def get_equipos(id_unidad):
    try:
        result = supabase.table("equipos").select("*").eq("id_unidad", id_unidad).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/equipos", methods=["POST"])
def crear_equipo():
    data = request.json
    try:
        result = supabase.table("equipos").insert({
            "nombre_equipo": data["nombre_equipo"],
            "id_unidad": data["id_unidad"]
        }).execute()

        equipo = result.data[0] if result.data else None

        # Si hay tareas existentes para la unidad, crear calificaciones iniciales (0.0) para este equipo
        if equipo:
            tareas = supabase.table("tareas").select("id_tarea").eq("id_unidad", equipo["id_unidad"]).execute()
            if tareas.data:
                inserts = []
                for t in tareas.data:
                    inserts.append({
                        "id_equipo": equipo["id_equipo"],
                        "id_tarea": t["id_tarea"],
                        "calificacion": 0.0
                    })
                if inserts:
                    supabase.table("calificaciones_equipos").insert(inserts).execute()

        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/equipos/<int:id_equipo>", methods=["PUT"])
def editar_equipo(id_equipo):
    data = request.json
    try:
        result = supabase.table("equipos").update({
            "nombre_equipo": data.get("nombre_equipo")
        }).eq("id_equipo", id_equipo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/equipos/<int:id_equipo>", methods=["DELETE"])
def eliminar_equipo(id_equipo):
    try:
        result = supabase.table("equipos").delete().eq("id_equipo", id_equipo).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/equipos/<int:id_equipo>/alumnos", methods=["GET"])
def get_alumnos_equipo(id_equipo):
    try:
        # obtener ids de alumnos en el equipo
        res = supabase.table("equipo_alumnos").select("id_alumno").eq("id_equipo", id_equipo).execute()
        if not res.data:
            return jsonify([]), 200
        ids = [r["id_alumno"] for r in res.data]
        # obtener datos completos de alumnos
        alumnos = supabase.table("alumnos").select("*").in_("id_alumno", ids).execute()
        return jsonify(alumnos.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#   ASIGNAR/REMOVER ALUMNOS A EQUIPOS
# =========================


@app.route("/api/equipos/<int:id_equipo>/alumnos", methods=["POST"])  # body: {id_alumno}
def asignar_alumno_equipo(id_equipo):
    data = request.json
    try:
        id_alumno = data["id_alumno"]
        # Insertar en equipo_alumnos (clave primaria compuesta evita duplicados)
        result = supabase.table("equipo_alumnos").insert({
            "id_equipo": id_equipo,
            "id_alumno": id_alumno
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/equipos/<int:id_equipo>/alumnos/<int:id_alumno>", methods=["DELETE"])
def remover_alumno_equipo(id_equipo, id_alumno):
    try:
        result = supabase.table("equipo_alumnos").delete().eq("id_equipo", id_equipo).eq("id_alumno", id_alumno).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#   RUTAS TAREAS
# =========================


@app.route("/api/tareas/<int:id_unidad>", methods=["GET"])
def get_tareas(id_unidad):
    try:
        result = supabase.table("tareas").select("*").eq("id_unidad", id_unidad).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tareas", methods=["POST"])  # Crear tarea y asignar a todos los equipos de la unidad
def crear_tarea():
    data = request.json
    try:
        result = supabase.table("tareas").insert({
            "nombre_tarea": data["nombre_tarea"],
            "descripcion": data.get("descripcion", None),
            "valor": data.get("valor", 1.0),
            "id_unidad": data["id_unidad"]
        }).execute()

        tarea = result.data[0] if result.data else None

        # Asignar la tarea a todos los equipos de la unidad (crear registros en calificaciones_equipos con 0.0)
        if tarea:
            equipos = supabase.table("equipos").select("id_equipo").eq("id_unidad", tarea["id_unidad"]).execute()
            inserts = []
            if equipos.data:
                for e in equipos.data:
                    inserts.append({
                        "id_equipo": e["id_equipo"],
                        "id_tarea": tarea["id_tarea"],
                        "calificacion": 0.0
                    })
            if inserts:
                supabase.table("calificaciones_equipos").insert(inserts).execute()

        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tareas/<int:id_tarea>", methods=["PUT"])
def editar_tarea(id_tarea):
    data = request.json
    try:
        result = supabase.table("tareas").update({
            "nombre_tarea": data.get("nombre_tarea"),
            "descripcion": data.get("descripcion"),
            "valor": data.get("valor")
        }).eq("id_tarea", id_tarea).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tareas/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    try:
        # Al eliminar la tarea, las calificaciones_equipos se eliminarán por cascada si la BD lo permite
        result = supabase.table("tareas").delete().eq("id_tarea", id_tarea).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#   RUTAS CALIFICACIONES EQUIPOS
# =========================


@app.route("/api/calificaciones", methods=["POST"])  # body: {id_equipo, id_tarea, calificacion}
def registrar_calificacion_equipo():
    data = request.json
    try:
        # Intentar actualizar si existe, sino insertar
        exists = supabase.table("calificaciones_equipos").select("*").eq("id_equipo", data["id_equipo"]).eq("id_tarea", data["id_tarea"]).execute()
        if exists.data:
            res = supabase.table("calificaciones_equipos").update({"calificacion": data["calificacion"]}).eq("id_equipo", data["id_equipo"]).eq("id_tarea", data["id_tarea"]).execute()
        else:
            res = supabase.table("calificaciones_equipos").insert({
                "id_equipo": data["id_equipo"],
                "id_tarea": data["id_tarea"],
                "calificacion": data["calificacion"]
            }).execute()

        # Después de registrar la calificación del equipo, recalcular la calificación final de la unidad para los alumnos del equipo
        # Obtener alumnos del equipo
        alumnos = supabase.table("equipo_alumnos").select("id_alumno").eq("id_equipo", data["id_equipo"]).execute()
        # Obtener id_unidad desde la tarea
        tarea = supabase.table("tareas").select("id_unidad").eq("id_tarea", data["id_tarea"]).execute()
        if tarea.data and alumnos.data:
            id_unidad = tarea.data[0]["id_unidad"]
            for a in alumnos.data:
                calcular_calificacion_final(id_unidad, a["id_alumno"])  # actualizar por alumno

        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/calificaciones/equipo/<int:id_equipo>", methods=["GET"])
def obtener_calificaciones_equipo(id_equipo):
    try:
        res = supabase.table("calificaciones_equipos").select("*").eq("id_equipo", id_equipo).execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/calificaciones/tarea/<int:id_tarea>", methods=["GET"])
def obtener_calificaciones_tarea(id_tarea):
    try:
        res = supabase.table("calificaciones_equipos").select("*").eq("id_tarea", id_tarea).execute()
        return jsonify(res.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
#   CALCULO CALIFICACION FINAL POR ALUMNO
# =========================


def calcular_calificacion_final(id_unidad, id_alumno):
    try:
        # Buscar equipos de la unidad
        equipos_unidad = supabase.table("equipos").select("id_equipo").eq("id_unidad", id_unidad).execute()
        if not equipos_unidad.data:
            return None

        equipo_ids = [e["id_equipo"] for e in equipos_unidad.data]

        # Encontrar el equipo al que pertenece el alumno dentro de esa unidad
        pertenencia = supabase.table("equipo_alumnos").select("id_equipo").eq("id_alumno", id_alumno).in_("id_equipo", equipo_ids).execute()
        if not pertenencia.data:
            return None

        id_equipo = pertenencia.data[0]["id_equipo"]

        # Obtener todas las tareas de la unidad con su valor
        tareas = supabase.table("tareas").select("id_tarea", "valor").eq("id_unidad", id_unidad).execute()
        if not tareas.data:
            return None

        tarea_ids = [t["id_tarea"] for t in tareas.data]

        # Obtener calificaciones del equipo en esas tareas (id_tarea + calificacion)
        califs = supabase.table("calificaciones_equipos").select("id_tarea", "calificacion").eq("id_equipo", id_equipo).in_("id_tarea", tarea_ids).execute()

        # Mapear calificaciones por id_tarea
        cal_map = {}
        if califs.data:
            for c in califs.data:
                try:
                    cal_map[c["id_tarea"]] = float(c.get("calificacion", 0.0))
                except Exception:
                    cal_map[c["id_tarea"]] = 0.0

        # Sumar ponderada: para cada tarea usar (valor/100) * calificacion_del_equipo
        total = 0.0
        for t in tareas.data:
            vid = t.get("id_tarea")
            valor = t.get("valor") or 0.0
            try:
                peso = float(valor) / 100.0
            except Exception:
                peso = 0.0
            cal_equipo = cal_map.get(vid, 0.0)
            total += peso * float(cal_equipo)

        promedio = total

        # Upsert en calificacion_unidad (unique por id_alumno, id_unidad)
        existe = supabase.table("calificacion_unidad").select("*").eq("id_alumno", id_alumno).eq("id_unidad", id_unidad).execute()
        if existe.data:
            supabase.table("calificacion_unidad").update({"calificacion_final": promedio}).eq("id_alumno", id_alumno).eq("id_unidad", id_unidad).execute()
        else:
            supabase.table("calificacion_unidad").insert({
                "id_alumno": id_alumno,
                "id_unidad": id_unidad,
                "calificacion_final": promedio
            }).execute()

        return promedio
    except Exception as e:
        print("Error calcular_calificacion_final:", e)
        return None


@app.route("/api/calificacion_unidad/calc/<int:id_unidad>", methods=["POST"])  # recalcula para todos los alumnos de la unidad
def recalcular_unidad(id_unidad):
    try:
        # Obtener alumnos del grupo (por medio de unidades->grupo)
        unidad = supabase.table("unidades").select("id_grupo").eq("id_unidad", id_unidad).execute()
        if not unidad.data:
            return jsonify({"error": "Unidad no encontrada"}), 404

        id_grupo = unidad.data[0]["id_grupo"]
        alumnos = supabase.table("alumnos").select("id_alumno").eq("id_grupo", id_grupo).execute()
        resultados = []
        if alumnos.data:
            for a in alumnos.data:
                prom = calcular_calificacion_final(id_unidad, a["id_alumno"])
                resultados.append({"id_alumno": a["id_alumno"], "calificacion_final": prom})

        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/calificacion_unidad/<int:id_unidad>/<int:id_alumno>", methods=["GET"])
def obtener_calificacion_unidad(id_unidad, id_alumno):
    try:
        res = supabase.table("calificacion_unidad").select("*").eq("id_unidad", id_unidad).eq("id_alumno", id_alumno).execute()
        if not res.data:
            # Calcular a la demanda
            prom = calcular_calificacion_final(id_unidad, id_alumno)
            if prom is None:
                return jsonify({"error": "Sin datos para calcular"}), 404
            return jsonify({"id_alumno": id_alumno, "id_unidad": id_unidad, "calificacion_final": prom}), 200
        return jsonify(res.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    threading.Timer(2.0, abrir_navegador).start()
    app.run(debug=True)