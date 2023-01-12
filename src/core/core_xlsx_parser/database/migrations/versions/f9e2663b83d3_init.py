"""init

Revision ID: f9e2663b83d3
Revises: 
Create Date: 2023-01-10 00:49:27.521472

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'f9e2663b83d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('all', sa.BigInteger(), nullable=True),
    sa.Column('man', sa.BigInteger(), nullable=True),
    sa.Column('woman', sa.BigInteger(), nullable=True),
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('man_perc', sa.Float(), nullable=True),
    sa.Column('woman_perc', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_people_guid'), 'people', ['guid'], unique=False)
    op.create_table('population',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('urban_people', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('rural_people', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['rural_people'], ['people.guid'], ),
    sa.ForeignKeyConstraint(['urban_people'], ['people.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_population_guid'), 'population', ['guid'], unique=False)
    op.create_table('country',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('population', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['population'], ['population.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_country_guid'), 'country', ['guid'], unique=False)
    op.create_table('federal_district',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('country_guid', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('population', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['country_guid'], ['country.guid'], ),
    sa.ForeignKeyConstraint(['population'], ['population.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_federal_district_guid'), 'federal_district', ['guid'], unique=False)
    op.create_table('some_region',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('district_guid', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('population', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['district_guid'], ['federal_district.guid'], ),
    sa.ForeignKeyConstraint(['population'], ['population.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_some_region_guid'), 'some_region', ['guid'], unique=False)
    op.create_table('autonomic_district',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('region_guid', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('population', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['population'], ['population.guid'], ),
    sa.ForeignKeyConstraint(['region_guid'], ['some_region.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_autonomic_district_guid'), 'autonomic_district', ['guid'], unique=False)
    op.create_table('local_subject',
    sa.Column('guid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('region_guid', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('people', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['people'], ['people.guid'], ),
    sa.ForeignKeyConstraint(['region_guid'], ['some_region.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_local_subject_guid'), 'local_subject', ['guid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_local_subject_guid'), table_name='local_subject')
    op.drop_table('local_subject')
    op.drop_index(op.f('ix_autonomic_district_guid'), table_name='autonomic_district')
    op.drop_table('autonomic_district')
    op.drop_index(op.f('ix_some_region_guid'), table_name='some_region')
    op.drop_table('some_region')
    op.drop_index(op.f('ix_federal_district_guid'), table_name='federal_district')
    op.drop_table('federal_district')
    op.drop_index(op.f('ix_country_guid'), table_name='country')
    op.drop_table('country')
    op.drop_index(op.f('ix_population_guid'), table_name='population')
    op.drop_table('population')
    op.drop_index(op.f('ix_people_guid'), table_name='people')
    op.drop_table('people')
    # ### end Alembic commands ###