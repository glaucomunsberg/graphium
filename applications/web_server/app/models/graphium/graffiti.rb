class Graphium::Graffiti
  include Mongoid::Document
  field :city, type: String
  field :state, type: String
  field :lat, type: Float
  field :lng, type: Float
  field :country, type: String
  field :pitch, type: Integer
  field :heading, type: String
  field :address, type: String
  field :pano_id, type: String
  field :situation, type: String

  store_in collection: "graffiti", database: "graphium"
end
