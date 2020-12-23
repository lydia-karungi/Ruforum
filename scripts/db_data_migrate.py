#--------------------------------------------------------------------------------------
#The purpose of this program is to help move data from the old system database to the new implementation
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# REST of app...
#--------------------------------------------------------------------------------------
from django.db import connections, connection
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
import re

OLD_DB = 'ruforum_old'
NEW_DB = 'ruforum'

def is_RelationalField(Model, field_name):
        return Model._meta.get_field(field_name).is_relation


def sanitize_fields(fields, Model):
    return list(map(lambda x: re.sub('_id$','',x) if is_RelationalField(Model,x) else x, fields))

def truncate(cursor, table_name):
    query = '''
    SET FOREIGN_KEY_CHECKS=0;
    TRUNCATE %(table)s;
    SET FOREIGN_KEY_CHECKS=1;
    ''' % {'table': table_name}
    cursor.execute(query)

def update_auto_increment(cursor, table_name):
    query = '''
    SET @m = (SELECT MAX(id) + 1 FROM %(table)s);
    SET @s = CONCAT('ALTER TABLE %(table)s AUTO_INCREMENT=', @m);
    PREPARE stmt1 FROM @s;
    EXECUTE stmt1;
    DEALLOCATE PREPARE stmt1;''' % {'table': table_name}
    cursor.execute(query)

def disable_auto_increment(cursor, table_name):
    query = '''
    SET FOREIGN_KEY_CHECKS=0;
    ALTER TABLE %(table)s MODIFY COLUMN id INT(11) NOT NULL;
    SET FOREIGN_KEY_CHECKS=1;
    ''' % {'table': table_name}
    cursor.execute(query)

def enable_auto_increment(cursor, table_name):
    query = '''
    SET FOREIGN_KEY_CHECKS=0;
    ALTER TABLE %(table)s MODIFY COLUMN id INT(11) NOT NULL AUTO_INCREMENT;
    SET FOREIGN_KEY_CHECKS=1;
    ''' % {'table': table_name}
    cursor.execute(query)


def get_fields(cursor, table_name, schema=NEW_DB):
    query = '''
    SELECT GROUP_CONCAT(COLUMN_NAME) AS FIELDS FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%(schema)s'  AND TABLE_NAME = '%(table)s'
    ''' % {'table': table_name, 'schema': schema}
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0]


def lookUpInstance(Model,field_name,pk):
    try:
        return Model._meta.get_field(field_name).related_model._meta.model.objects.get(pk=pk)
    except:
        return pk


def migrate(Model, table_name, src_schema):
    model_name = Model._meta.model_name
    table_name = table_name
    print("------------------ MIGRATING %s DATA ------------------------" % model_name)
    with connection.cursor() as nu_cursor: # for access to the new db to which we'll write using raw sql somewhere
        with connections['old_db'].cursor() as cursor: # for access to the old db from which we'll read using raw sql
            truncate(nu_cursor,table_name)
            disable_auto_increment(nu_cursor,table_name)
            sfields = get_fields(cursor, table_name, schema=src_schema) #dynamically determine fields
            fields = sfields.split(",")
            print('SELECT %(fields)s from %(table)s' % {'fields': sfields, 'table': table_name})
            cursor.execute('SELECT %(fields)s from %(table)s' % {'fields': sfields, 'table': table_name})
            print("Starting...")
            for row in cursor.fetchall():
                dfields = dict(zip(sanitize_fields(fields,Model), [lookUpInstance(Model,f,row[fields.index(f)]) if is_RelationalField(Model,f) else row[fields.index(f)] for f in fields]))
                print(dfields)
                print("Processing %s: " % model_name, row[0])
                instance,created = Model.objects.get_or_create(**dfields)
                print("%s " % "Created >> " if created else "Found :: ", instance)
            enable_auto_increment(nu_cursor,table_name)
            update_auto_increment(nu_cursor,table_name)
            print("Finished.")


def run():
    from contacts.models import User,Student, Studentfundingsource
    from django_comments.models import Comment
    from custom_comments.models import Ruforumcomment
    from grant_types.models import Granttype
    from grants_applications.models import Collaborator, Grantapplication

    # following example shows when we might use new database schema as the reference when doing auto-migration
    #migrate(Call, 'calls_call','ruforum')
    # the example below uses the old schema as the reference instead... (thus far, this seems to work best for most models)
    # note that when merely looking at new schema, some quirky things are found: 'countries' <-- doesn't seem to have an associated model though table exists in both new and old rims!

    #---------------- let's automate everything then!

    # let's get a mapping of all available models to their table names
    from django.apps import apps
    model_table_map = {} # will have structure: {table_name: model_class}
    all_models = apps.get_models()
    summary = []
    summary.append("----- Found %s models. Auto-migration starting..." % (len(all_models)))
    print("----- Found %s models. Auto-migration starting..." % (len(all_models)))
    for model in all_models:
        model_table_name = model._meta.db_table
        model_table_map[model_table_name] = model

    all_old_rims_tables = ["auth_group","auth_group_permissions","auth_permission","calls_call","contacts_student","contacts_studentfundingsource","contacts_user","contacts_user_groups","contacts_user_user_permissions","countries","custom_comments_ruforumcomment","django_admin_log","django_comment_flags","django_comments","django_content_type","django_migrations","django_session","django_site","easy_thumbnails_source","easy_thumbnails_thumbnail","easy_thumbnails_thumbnaildimensions","events_event","events_event_participants","grant_types_granttype","grants_applications_collaborator","grants_applications_commodityfocus","grants_applications_grantapplication","grants_applications_grantapplication_reviewers","grants_applications_grantappreview","grants_applications_subtheme","grants_applications_supportingletter","grants_applications_theme","grants_grant","grants_reports_month12report","grants_reports_month18report","grants_reports_month24report","grants_reports_month30report","grants_reports_month6report","grants_reports_studentmonth12report","grants_reports_studentmonth18report","grants_reports_studentmonth24report","grants_reports_studentmonth30report","grants_reports_studentmonth6report","grants_studentmembership","registration_registrationprofile","scholarships_additionalfundingsource","scholarships_communityservice","scholarships_currentvolunteering","scholarships_employmenthistory","scholarships_groupassociationclub","scholarships_homeassets","scholarships_householdincomesource","scholarships_incomecontributor","scholarships_leadershipposition","scholarships_mastercardeducation","scholarships_mastercardscholarshipapplication","scholarships_mastercardscholarshipapplication_home_assets","scholarships_mastercardscholarshipapplication_income_contrib3efc","scholarships_mastercardscholarshipapplication_type_of_floor","scholarships_mastercardscholarshipapplication_type_of_house_wall","scholarships_mastercardscholarshipapplication_type_of_roofing","scholarships_othereducation","scholarships_otherscholarshipapplication","scholarships_parent","scholarships_referenceletter","scholarships_scholarshipapplication","scholarships_scholarshipappreview","scholarships_transcriptfile","scholarships_typeoffloor","scholarships_typeofhousewall","scholarships_typeofroofingmaterial","scholarships_workexperience","south_migrationhistory","student_reports_briefsattachment","student_reports_manuscript","student_reports_mastercardalumnireport","student_reports_mastercardstudentreport","student_reports_milestone","student_reports_otherstudentreport","student_reports_publicationattachment","student_reports_skillenhancement","student_reports_studentreport","template_manager_template"]
    for table in model_table_map:
        try:
            if table in all_old_rims_tables:
                migrate(model_table_map[table], table, OLD_DB)
                #migrate(model_table_map[table], table, NEW_DB)
                summary.append("---> Migrated Model: %s | Table: %s " % (model_table_map[table], table))
            else:
                summary.append("---X MISSING Old Table for Model: %s | Table: %s " % (model_table_map[table], table))
        except Exception as e:
            print(e)
            try:
                #try with the new schema as the ref
                migrate(model_table_map[table], table, NEW_DB)
                summary.append("---> Migrated* Model: %s | Table: %s " % (model_table_map[table], table))
            except Exception as e1:
                print(e)
                summary.append("---X FAILED Migration for Model: %s | Table: %s " % (model_table_map[table], table))


    # show summary of ops performed...
    for msg in summary:
        print("%s" % msg)

