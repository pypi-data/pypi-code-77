"""Mars Rover database module."""

from pathlib import Path
from sqlite3 import connect

from IPython.core.display import HTML

from ..api import get_all
from ..image import RGB
from ..misc import logger, now


log_db, debug_db = logger('Database')


class RoverDatabase:
    """Rover database object.

    Parameters
    ----------
    fname: str or pathlib.Path
        Database filename.
    category: str
        API category name.

    """
    FIELDS = [
        ('instrument', 'TEXT'),
        ('sol', 'INTEGER'),
        ('imageid', 'TEXT'),
        ('date_taken_utc', 'TEXT'),
        ('date_taken_mars', 'TEXT'),
        ('date_received', 'TEXT'),
        ('sclk', 'TEXT'),
        ('dimension', 'TEXT'),
        ('filter_name', 'TEXT'),
        ('xyz', 'TEXT'),
        ('attitude', 'TEXT'),
        ('camera_vector', 'TEXT'),
        ('camera_model_component_list', 'TEXT'),
        ('camera_position', 'TEXT'),
        ('camera_model_type', 'TEXT'),
        ('subframeRect', 'TEXT'),
        ('scaleFactor', 'TEXT'),
        ('mastAz', 'TEXT'),
        ('mastEl', 'TEXT'),
        ('title', 'TEXT'),
        ('caption', 'TEXT'),
        ('sample_type', 'TEXT'),
        ('json_link', 'TEXT'),
        ('link', 'TEXT'),
        ('small', 'TEXT'),
        ('medium', 'TEXT'),
        ('large', 'TEXT'),
        ('full_res', 'TEXT'),
        ('drive', 'TEXT'),
        ('site', 'INTEGER'),
        ('credit', 'TEXT'),
    ]

    def __init__(self, fname, category):
        self.fname = Path(fname)
        self.category = category

        self.conn = connect(self.fname)
        self.cursor = self.conn.cursor()
        self.create_imgs_table()

        log_db.debug('Connect: %s', self.fname)

    def __repr__(self):
        n = self.count
        if n == 0:
            desc = 'EMPTY'
        else:
            desc = f'{n} image' + ('' if n > 1 else '')
            desc += f' | latest: {self.latest_img}'

        return f'<{self.__class__.__name__}> {desc}'

    def __call__(self, *args, show=False, **kwargs):
        if show:
            return self.show(**kwargs)

        return self.search(*args, **kwargs)

    def __contains__(self, other):
        return self.contains(other)

    def create_imgs_table(self):
        """Create Imgs table."""
        log_db.debug('Create tables (if not exists)')

        # Create Img table
        fields = ','.join([f'{field} {_type}' for field, _type, in self.FIELDS])
        sql = f'CREATE TABLE IF NOT EXISTS Imgs ({fields}, PRIMARY KEY("imageid"))'
        self.cursor.execute(sql)

        # Create Updates table
        sql = ('CREATE TABLE IF NOT EXISTS Updates ('
               'update_date, '
               'nb_new_imgs, '
               'nb_imgs_before, '
               'nb_imgs_after, '
               'old_latest_img, '
               'new_latest_img)')
        self.cursor.execute(sql)

    def delete_imgs_table(self):
        """Delete Imgs table."""
        log_db.warning('Remove all tables from %s', self.fname)

        sql = 'DROP TABLE IF EXISTS Imgs'
        self.cursor.execute(sql)

    def purge(self):
        """Purge Imgs database."""
        self.delete_imgs_table()
        self.create_imgs_table()

    def row(self, json):
        """Extract data from JSON."""
        default = {key: None for key, _ in self.FIELDS}
        default.update(json)
        return tuple(default.values())

    @property
    def insert_into(self):
        """SQL insert into statement."""
        return 'INSERT INTO Imgs VALUES (' + ','.join(len(self.FIELDS) * '?') + ')'

    def insert(self, json):
        """Insert data values."""
        nb_imgs_before = self.count
        old_latest_img = self.latest_img
        update_date = now()

        log_db.debug('Before: %i images | Latest: %s', nb_imgs_before, old_latest_img)

        if isinstance(json, list):
            self.cursor.executemany(self.insert_into, [self.row(img) for img in json])
        else:
            self.cursor.execute(self.insert_into, self.row(json))

        # Commit changes
        self.conn.commit()

        nb_imgs_after = self.count
        new_latest_img = self.latest_img
        nb_new_imgs = nb_imgs_after - nb_imgs_before

        log_db.info('%i images were added.', nb_new_imgs)
        log_db.debug('After: %i images | Latest: %s', nb_imgs_after, new_latest_img)

        # Save changes in update table
        row = tuple([
            update_date,
            nb_new_imgs,
            nb_imgs_before,
            nb_imgs_after,
            old_latest_img,
            new_latest_img,
        ])
        sql = 'INSERT INTO Updates VALUES (' + ','.join(len(row) * '?') + ')'

        self.cursor.execute(sql, row)
        self.conn.commit()

        log_db.debug('Update infos saved')

    def update(self, num=100):
        """Update the database content."""
        json = get_all(lastest=self.latest_img,
                       num=num,
                       category=self.category,
                       order='sol+desc')
        if json:
            self.insert(json)

    @property
    def count(self):
        """Count the number of images in the database."""
        self.cursor.execute('SELECT COUNT(imageid) from Imgs')
        return self.cursor.fetchone()[0]

    @property
    def imgs(self):
        """List of images id in the database."""
        self.cursor.execute('SELECT imageid from Imgs')
        return [img_id for (img_id,) in self.cursor.fetchall()]

    @property
    def latest_img(self):
        """Lastest image id added to the database."""
        self.cursor.execute('SELECT imageid from Imgs ORDER BY rowid DESC LIMIT 1')
        res = self.cursor.fetchone()
        return res[0] if res else None

    def contains(self, img_id):
        """check if a image is in the database."""
        self.cursor.execute(
            'SELECT COUNT(*) from Imgs WHERE imageid=? LIMIT 1', (img_id,))
        return self.cursor.fetchone()[0] == 1

    def search(self, fields='imageid', where=None, order=None, limit=None):
        """Search into the image database."""
        if isinstance(fields, (tuple, list)):
            fields = ', '.join(fields)

        sql = f'SELECT {fields} FROM Imgs'

        if where is not None:
            sql += f' WHERE {where}'

        if order is not None:
            sql += f' ORDER BY {order}'

        if limit is not None:
            sql += f' LIMIT {limit}'

        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        if not res:
            return []

        if len(res[0]) == 1:
            return [data for (data,) in res]

        return res

    def show(self, **kwargs):
        """Show images for a search requests."""
        style = ';'.join([
            'display: flex',
            'flex-direction: row',
            'flex-wrap: wrap',
            'justify-content: space-evenly',
            'align-items: baseline',
        ])
        html = f'<div style="{style}">'

        imgs = self.search(fields='imageid,small,full_res', **kwargs)

        for img_id, thumbnail, url in imgs:
            html += f'<a href="{url}" target="_blank">'
            html += f'<p style="text-align:center;font-size:10px">{img_id}</p>'
            html += f'<img src="{thumbnail}" style="margin:auto"/>'
            html += '</a>'

        html += '</div>'

        return HTML(html)

    def group_rgb(self):
        """Group RGB pairs."""
        sql = '''
SELECT
    rgb_name,
    group_concat(imageid) as image_ids,
    group_concat(channel) as channels,
    group_concat(full_res) as urls,
    count(imageid) AS nb,
    instrument,
    dimension,
    camera_vector,
    sol,
    attitude
FROM (
    SELECT
        *,
        substr(imageid, 3, 1) as channel,
        substr(imageid, 1, 1) || "_F" ||
        substr(imageid, 4) || "-" || substr(imageid, 2, 1) as rgb_name
    FROM Imgs
    WHERE
        camera_vector != "UNK"
    AND
        (channel  = "R" OR channel  = "G" OR channel  = "B")
    ORDER BY
        channel DESC,
        rgb_name
)
GROUP BY camera_vector, sol, attitude
HAVING nb > 1
ORDER BY
    nb DESC,
    sol
'''
        self.cursor.execute(sql)
        return [RGB(res) for res in self.cursor.fetchall()]

    def save_rgb(self, output_dir='RGB'):
        """Save all RGB in `output_dir`."""
        return [rgb.save(output_dir=output_dir) for rgb in self.group_rgb()]
