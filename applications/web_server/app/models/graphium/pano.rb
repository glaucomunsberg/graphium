class Graphium::Pano
  include Mongoid::Document
  field :imagem_name, type: String
  field :classification, type: String
  field :pano_id, type: String
  field :swarm_identifier, type: String
  field :splited, type: String
  field :heading, type: String
  field :pano_date, type: String

  store_in collection: "pano", database: "graphium"
end
