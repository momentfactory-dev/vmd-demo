# https://roksf0130.tistory.com/98

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
import json


def json_parse(data):
    # JSON 인코딩
    jsonString = json.dumps(data)
    print("jsonString      ->      ", jsonString)
    return json.loads(jsonString)


def load_ui(path):
    return render_template(path)


def load_ui_name(path, name):
    """

    <body>
        <h1> hello {{name}} </h1>
    </body>

    """
    return render_template(path, name=name)


def load_ui_marks(path, marks):
    """

    <body>
        {% if marks >= 50 %}
        <h1>Your result is pass</h1>
        {% else %}
        <h1>Your result is fail</h1>
        {% endif %}
    </body>

    """
    return render_template(path, marks=marks)


def load_ui_dict(path, dict):
    """

    <body>
        <table border=1>
            {% for key, value in result.iteritems() %}
            <tr>
                <th> {{key}} </th>
                <td> {{value}} </td>
            </tr>
            {% endfor %}
        </table>
    </body>

    """
    result = render_template(path, result=dict)
    return result
